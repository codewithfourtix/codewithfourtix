import datetime
from dateutil import relativedelta
import requests
import os
from lxml import etree
import time
import hashlib

HEADERS = {'authorization': 'token ' + os.environ['ACCESS_TOKEN']}
USER_NAME = os.environ['USER_NAME']  # Should be 'codewithfourtix'
QUERY_COUNT = {'user_getter': 0, 'follower_getter': 0, 'graph_repos_stars': 0, 'recursive_loc': 0, 'loc_query': 0}

def daily_readme(birthday):
    diff = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    return '{} {}, {} {}, {} {}{}'.format(
        diff.years, 'year' + format_plural(diff.years),
        diff.months, 'month' + format_plural(diff.months),
        diff.days, 'day' + format_plural(diff.days),
        ' 🎂' if (diff.months == 0 and diff.days == 0) else '')

def format_plural(unit):
    return 's' if unit != 1 else ''

def simple_request(func_name, query, variables):
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=HEADERS)
    if request.status_code != 200:
        print(f"HTTP Error in {func_name}: {request.status_code} - {request.text}")
        raise Exception(func_name, ' failed with status', request.status_code)
    data = request.json()
    if 'errors' in data:
        print(f"GraphQL Errors in {func_name}: {data['errors']}")
        raise Exception(func_name, ' GraphQL errors:', data['errors'])
    if 'data' not in data:
        raise Exception(func_name, ' No data in response')
    return request

def graph_repos_stars(count_type, owner_affiliation, cursor=None, total=0):
    query_count('graph_repos_stars')
    query = '''
    query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
        user(login: $login) {
            repositories(first: 100, after: $cursor, ownerAffiliations: $owner_affiliation) {
                totalCount
                edges {
                    node {
                        ... on Repository {
                            nameWithOwner
                            stargazers {
                                totalCount
                            }
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }'''
    variables = {'owner_affiliation': owner_affiliation, 'login': USER_NAME, 'cursor': cursor}
    request = simple_request(graph_repos_stars.__name__, query, variables)
    repos_data = request.json()['data']['user']['repositories']
    if count_type == 'repos':
        return repos_data['totalCount']
    elif count_type == 'stars':
        total += stars_counter(repos_data['edges'])
        if repos_data['pageInfo']['hasNextPage']:
            return graph_repos_stars(count_type, owner_affiliation, repos_data['pageInfo']['endCursor'], total)
        return total

def stars_counter(data):
    return sum(node['node']['stargazers']['totalCount'] for node in data if node['node'])

# LOC functions unchanged except added safety in loc_query
def recursive_loc(owner, repo_name, data, cache_comment, addition_total=0, deletion_total=0, my_commits=0, cursor=None):
    query_count('recursive_loc')
    query = '''
    query ($repo_name: String!, $owner: String!, $cursor: String) {
        repository(name: $repo_name, owner: $owner) {
            defaultBranchRef {
                target {
                    ... on Commit {
                        history(first: 100, after: $cursor) {
                            totalCount
                            edges {
                                node {
                                    ... on Commit {
                                        committedDate
                                    }
                                    author {
                                        user {
                                            id
                                        }
                                    }
                                    deletions
                                    additions
                                }
                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                }
            }
        }
    }'''
    variables = {'repo_name': repo_name, 'owner': owner, 'cursor': cursor}
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=HEADERS)
    if request.status_code == 200:
        repo_data = request.json().get('data', {}).get('repository', {})
        if repo_data.get('defaultBranchRef') is not None:
            history = repo_data['defaultBranchRef']['target']['history']
            return loc_counter_one_repo(owner, repo_name, data, cache_comment, history, addition_total, deletion_total, my_commits)
        else:
            return 0
    force_close_file(data, cache_comment)
    raise Exception('recursive_loc failed', request.status_code, request.text)

def loc_counter_one_repo(owner, repo_name, data, cache_comment, history, addition_total, deletion_total, my_commits):
    for node in history['edges']:
        author_user = node['node']['author'].get('user')
        if author_user and author_user['id'] == OWNER_ID['id']:
            my_commits += 1
            addition_total += node['node']['additions']
            deletion_total += node['node']['deletions']
    if not history['pageInfo']['hasNextPage']:
        return addition_total, deletion_total, my_commits
    return recursive_loc(owner, repo_name, data, cache_comment, addition_total, deletion_total, my_commits, history['pageInfo']['endCursor'])

def loc_query(owner_affiliation, comment_size=0, force_cache=False, cursor=None, edges=[]):
    query_count('loc_query')
    query = '''
    query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
        user(login: $login) {
            repositories(first: 60, after: $cursor, ownerAffiliations: $owner_affiliation) {
                edges {
                    node {
                        ... on Repository {
                            nameWithOwner
                            defaultBranchRef {
                                target {
                                    ... on Commit {
                                        history {
                                            totalCount
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }'''
    variables = {'owner_affiliation': owner_affiliation, 'login': USER_NAME, 'cursor': cursor}
    try:
        request = simple_request(loc_query.__name__, query, variables)
        repos_data = request.json()['data']['user']['repositories']
        if repos_data['pageInfo']['hasNextPage']:
            edges += repos_data['edges']
            return loc_query(owner_affiliation, comment_size, force_cache, repos_data['pageInfo']['endCursor'], edges)
        else:
            return cache_builder(edges + repos_data['edges'], comment_size, force_cache)
    except Exception as e:
        print("LOC query failed (common with fine-grained tokens):", str(e))
        print("Falling back to zero LOC stats.")
        return [0, 0, 0, True]  # add, del, total, cached=True

# cache_builder, flush_cache, force_close_file, svg_overwrite, justify_format, find_and_replace, commit_counter unchanged

def svg_overwrite(filename, age_data, commit_data, star_data, repo_data, contrib_data, follower_data, loc_data):
    tree = etree.parse(filename)
    root = tree.getroot()
    justify_format(root, 'age_data', age_data, 22)
    justify_format(root, 'commit_data', commit_data, 17)
    justify_format(root, 'star_data', star_data, 11)
    justify_format(root, 'repo_data', repo_data, 4)
    justify_format(root, 'contrib_data', contrib_data)
    justify_format(root, 'follower_data', follower_data, 7)
    justify_format(root, 'loc_data', loc_data[2], 1)
    justify_format(root, 'loc_add', loc_data[0])
    justify_format(root, 'loc_del', loc_data[1], 1)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

# Rest of functions (commit_counter, user_getter, follower_getter, etc.) remain the same

if __name__ == '__main__':
    print('Calculation times:')
    user_data, user_time = perf_counter(user_getter, USER_NAME)
    global OWNER_ID
    OWNER_ID, _ = user_data
    formatter('account data', user_time)

    # CHANGE THIS TO YOUR ACTUAL BIRTHDAY (year, month, day)
    age_data, age_time = perf_counter(daily_readme, datetime.datetime(2005, 7, 25))  # Example: datetime.datetime(2000, 1, 1)
    formatter('age calculation', age_time)

    total_loc, loc_time = perf_counter(loc_query, ['OWNER'], 7)
    formatter('LOC (cached)', loc_time) if total_loc[-1] else formatter('LOC (no cache)', loc_time)

    commit_data, commit_time = perf_counter(commit_counter, 7)
    formatter('commit data', commit_time)

    star_data, star_time = perf_counter(graph_repos_stars, 'stars', ['OWNER'])
    formatter('stars count', star_time)

    repo_data, repo_time = perf_counter(graph_repos_stars, 'repos', ['OWNER'])
    formatter('repos count', repo_time)

    contrib_data, contrib_time = perf_counter(graph_repos_stars, 'repos', ['OWNER', 'COLLABORATOR', 'ORGANIZATION_MEMBER'])
    formatter('contributed repos', contrib_time)

    follower_data, follower_time = perf_counter(follower_getter, USER_NAME)
    formatter('followers count', follower_time)

    for index in range(len(total_loc)-1):
        total_loc[index] = '{:,}'.format(total_loc[index])

    svg_overwrite('dark_mode.svg', age_data, commit_data, star_data, repo_data, contrib_data, follower_data, total_loc[:-1])
    svg_overwrite('light_mode.svg', age_data, commit_data, star_data, repo_data, contrib_data, follower_data, total_loc[:-1])

    total_func_time = user_time + age_time + loc_time + commit_time + star_time + repo_time + contrib_time + follower_time
    print('\033[F' * 10,
          '{:<21}'.format('Total function time:'), '{:>11}'.format('%.4f' % total_func_time),
          ' s \033[E' * 10, sep='')

    print('Total GitHub GraphQL API calls:', '{:>3}'.format(sum(QUERY_COUNT.values())))
    for funct_name, count in QUERY_COUNT.items():
        print('{:<28}'.format('   ' + funct_name + ':'), '{:>6}'.format(count))