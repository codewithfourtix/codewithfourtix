import datetime
from dateutil import relativedelta
import requests
import os
from lxml import etree
import time
import hashlib

HEADERS = {'authorization': 'token ' + os.environ['ACCESS_TOKEN']}
USER_NAME = os.environ['USER_NAME']
QUERY_COUNT = {'user_getter': 0, 'follower_getter': 0, 'graph_repos_stars': 0, 'recursive_loc': 0, 'graph_commits': 0, 'loc_query': 0}

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
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables':variables}, headers=HEADERS)
    if request.status_code == 200:
        return request
    raise Exception(func_name, ' has failed with a', request.status_code, request.text, QUERY_COUNT)

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
    data = request.json()['data']['user']['repositories']
    if count_type == 'repos':
        return data['totalCount']
    elif count_type == 'stars':
        total += stars_counter(data['edges'])
        if data['pageInfo']['hasNextPage']:
            return graph_repos_stars(count_type, owner_affiliation, data['pageInfo']['endCursor'], total)
        return total

def stars_counter(data):
    total_stars = 0
    for node in data: total_stars += node['node']['stargazers']['totalCount']
    return total_stars

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

def justify_format(root, element_id, new_text, length=0):
    if isinstance(new_text, int):
        new_text = f"{'{:,}'.format(new_text)}"
    new_text = str(new_text)
    find_and_replace(root, element_id, new_text)
    just_len = max(0, length - len(new_text))
    if just_len <= 2:
        dot_map = {0: '', 1: ' ', 2: '. '}
        dot_string = dot_map[just_len]
    else:
        dot_string = ' ' + ('.' * just_len) + ' '
    find_and_replace(root, f"{element_id}_dots", dot_string)

def find_and_replace(root, element_id, new_text):
    element = root.find(f".//*[@id='{element_id}']")
    if element is not None:
        element.text = new_text

def commit_counter(comment_size):
    total_commits = 0
    filename = 'cache/'+hashlib.sha256(USER_NAME.encode('utf-8')).hexdigest()+'.txt'
    if not os.path.exists(filename): return 0
    with open(filename, 'r') as f:
        data = f.readlines()
    for line in data[comment_size:]:
        total_commits += int(line.split()[2])
    return total_commits

def user_getter(username):
    query_count('user_getter')
    query = '''
    query($login: String!){
        user(login: $login) {
            id
            createdAt
        }
    }'''
    variables = {'login': username}
    request = simple_request(user_getter.__name__, query, variables)
    return {'id': request.json()['data']['user']['id']}, request.json()['data']['user']['createdAt']

def follower_getter(username):
    query_count('follower_getter')
    query = '''
    query($login: String!){
        user(login: $login) {
            followers {
                totalCount
            }
        }
    }'''
    request = simple_request(follower_getter.__name__, query, {'login': username})
    return int(request.json()['data']['user']['followers']['totalCount'])

def query_count(funct_id):
    global QUERY_COUNT
    QUERY_COUNT[funct_id] += 1

# Moved perf_counter and formatter here (before main)
def perf_counter(funct, *args):
    start = time.perf_counter()
    funct_return = funct(*args)
    return funct_return, time.perf_counter() - start

def formatter(query_type, difference, funct_return=False, whitespace=0):
    print('{:<23}'.format('   ' + query_type + ':'), sep='', end='')
    print('{:>12}'.format('%.4f' % difference + ' s ')) if difference > 1 else print('{:>12}'.format('%.4f' % (difference * 1000) + ' ms'))
    if whitespace:
        return f"{'{:,}'.format(funct_return): <{whitespace}}"
    return funct_return

if __name__ == '__main__':
    print('Calculation times:')
    user_data, user_time = perf_counter(user_getter, USER_NAME)
    global OWNER_ID
    OWNER_ID, acc_date = user_data
    formatter('account data', user_time)

    # CHANGE THIS TO YOUR ACTUAL BIRTHDAY (year, month, day)
    age_data, age_time = perf_counter(daily_readme, datetime.datetime(2005, 7, 26)) 
    formatter('age calculation', age_time)

    # LOC disabled to avoid crashes
    total_loc = ['0', '0', '0', True]
    loc_time = 0.0  # dummy for total time calculation

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
        total_loc[index] = '{:,}'.format(int(total_loc[index]))

    svg_overwrite('dark_mode.svg', age_data, commit_data, star_data, repo_data, contrib_data, follower_data, total_loc[:-1])
    svg_overwrite('light_mode.svg', age_data, commit_data, star_data, repo_data, contrib_data, follower_data, total_loc[:-1])

    total_func_time = user_time + age_time + loc_time + commit_time + star_time + repo_time + contrib_time + follower_time
    print('\033[F'*10,
          '{:<21}'.format('Total function time:'), '{:>11}'.format('%.4f' % total_func_time),
          ' s \033[E'*10, sep='')

    print('Total GitHub GraphQL API calls:', '{:>3}'.format(sum(QUERY_COUNT.values())))
    for funct_name, count in QUERY_COUNT.items():
        print('{:<28}'.format('   ' + funct_name + ':'), '{:>6}'.format(count))