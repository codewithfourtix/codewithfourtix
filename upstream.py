"""Build the open source section of the profile README from public pull requests.

The README build runs this every day. Merges that GitHub does not record, such as
Copybara imports, and fixes folded into a maintainer's pull request are listed in
upstream.json, along with the organizations to feature and a line about each fix.
"""

import base64
import datetime
import html
import json
import os
from pathlib import Path

import requests

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
README = ROOT / "README.md"
START = "<!-- upstream:start -->"
END = "<!-- upstream:end -->"

LANDED = ("merged", "landed", "co-authored")
STATUS_ORDER = {"merged": 0, "landed": 0, "co-authored": 1, "open": 2, "closed": 3}

THEMES = {
    "dark": {"bg": "#161b22", "rule": "#30363d", "tile": "#21262d", "ink": "#e6edf3", "muted": "#8b949e",
             "accent": "#ffa657"},
    "light": {"bg": "#ffffff", "rule": "#d0d7de", "tile": "#f6f8fa", "ink": "#1f2328", "muted": "#59636e",
              "accent": "#bc4c00"},
}
FONTS = {
    "display": ASSETS / "fonts" / "archivo-extracondensed-extrabold.woff2",
    "body": ASSETS / "fonts" / "archivo-regular.woff2",
    "mono": ASSETS / "fonts" / "ibm-plex-mono-regular.woff2",
}
METRICS = json.loads((ASSETS / "fonts" / "metrics.json").read_text(encoding="utf-8"))

WIDTH = 1200
LEFT = 56
RIGHT = WIDTH - LEFT
TILE = 64
NAME_X = LEFT + TILE + 24
NAME_SIZE = 46
SAYS_X = 470
SAYS_WIDTH = RIGHT - SAYS_X
TAG_WIDTH = 110
SAYS_SIZE = 21
MONO_SIZE = 15


def fetch_pull_requests(user, token):
    """Return every public pull request opened by user."""
    prs, page = [], 1
    while True:
        response = requests.get(
            "https://api.github.com/search/issues",
            params={"q": f"is:pr author:{user} is:public", "per_page": 100, "page": page},
            headers={"Authorization": f"token {token}", "Accept": "application/vnd.github+json"},
            timeout=30,
        )
        response.raise_for_status()
        items = response.json()["items"]
        prs += [
            {
                "repo": item["repository_url"].split("/repos/", 1)[1],
                "number": item["number"],
                "title": item["title"],
                "url": item["html_url"],
                "state": item["state"],
                "merged": bool(item["pull_request"].get("merged_at")),
            }
            for item in items
        ]
        if len(items) < 100:
            return prs
        page += 1


def ref(pr):
    return f"{pr['repo']}#{pr['number']}"


def status(pr, config):
    """Return merged, landed, co-authored, open or closed."""
    if pr["merged"]:
        return "merged"
    if ref(pr) in config["landed"]:
        return "landed"
    if ref(pr) in config["coauthored"]:
        return "co-authored"
    return pr["state"]


def status_label(pr, config):
    """Describe the status of a pull request for the README tables."""
    if pr["status"] == "landed":
        return config["landed"][ref(pr)]
    if pr["status"] == "co-authored":
        repo, number = config["coauthored"][ref(pr)].split("#")
        return f"co-authored in [#{number}](https://github.com/{repo}/pull/{number})"
    return pr["status"]


def repo_refs(name, prs):
    """Name the pull requests of each repository, the busiest repository first."""
    by_repo = {}
    for pr in sorted(prs, key=lambda pr: pr["number"]):
        by_repo.setdefault(pr["repo"].split("/")[1], []).append(pr["number"])
    parts = []
    for repo, numbers in sorted(by_repo.items(), key=lambda item: (-len(item[1]), item[0].lower())):
        label = "" if repo == name else f"{repo} "
        if len(numbers) > 3:
            parts.append(f"{label}{len(numbers)} pull requests")
        else:
            parts.append(label + " ".join(f"#{number}" for number in numbers))
    return parts


def headline(prs, config):
    """The configured line about the first highlighted pull request, else the newest title."""
    refs = {ref(pr) for pr in prs}
    for highlight in config["highlights"]:
        if highlight["pr"] in refs:
            return highlight["says"]
    return max(prs, key=lambda pr: pr["number"])["title"]


def organization_rows(prs, config):
    """One row per configured organization: merged work first, then work in review."""
    merged, review = [], []
    for organization in config["organizations"]:
        theirs = [pr for pr in prs if pr["repo"].startswith(tuple(organization["repos"]))]
        done = [pr for pr in theirs if pr["status"] in LANDED]
        pending = [pr for pr in theirs if pr["status"] == "open"]
        shown = done or pending
        if shown:
            (merged if done else review).append({
                "name": organization["name"],
                "logo": organization["logo"],
                "merged": bool(done),
                "refs": repo_refs(organization["name"], shown),
                "says": headline(shown, config),
            })
    return merged + review


def text_width(text, font, size):
    metrics = METRICS[font]
    advances = metrics["advances"]
    return sum(advances.get(char, advances["n"]) for char in text) * size / metrics["units_per_em"]


def wrap(text, font, size, width):
    """Break text into lines no wider than width."""
    lines = [""]
    for word in text.split():
        candidate = f"{lines[-1]} {word}".strip()
        if lines[-1] and text_width(candidate, font, size) > width:
            lines.append(word)
        else:
            lines[-1] = candidate
    return lines


def fit_refs(parts, width):
    """Join as many parts as fit in width, counting the rest as more."""
    for count in range(len(parts), 0, -1):
        rest = len(parts) - count
        text = "   ".join(parts[:count] + ([f"+{rest} more"] if rest else []))
        if text_width(text, "mono", MONO_SIZE) <= width:
            return text
    return ""


def font_face(family, path):
    data = base64.b64encode(path.read_bytes()).decode()
    return f'@font-face{{font-family:"{family}";src:url(data:font/woff2;base64,{data}) format("woff2")}}'


def logo_tile(row, index, x, y, theme):
    """The organization's GitHub avatar on a rounded tile, or its initial when it has none."""
    shape = f'x="{x}" y="{y}" width="{TILE}" height="{TILE}" rx="14"'
    if row["logo"] is None:
        return (
            f'<rect {shape} fill="{theme["tile"]}" stroke="{theme["rule"]}"/>'
            f'<text class="d" x="{x + TILE / 2}" y="{y + TILE / 2 + 15}" text-anchor="middle" font-size="42" '
            f'fill="{theme["ink"]}">{html.escape(row["name"][0])}</text>'
        )
    data = base64.b64encode((ASSETS / "logos" / f"{row['logo']}.png").read_bytes()).decode()
    return (
        f'<clipPath id="tile{index}"><rect {shape}/></clipPath>'
        f'<rect {shape} fill="#ffffff"/>'
        f'<image href="data:image/png;base64,{data}" x="{x}" y="{y}" width="{TILE}" height="{TILE}" '
        f'clip-path="url(#tile{index})"/>'
        f'<rect {shape} fill="none" stroke="{theme["rule"]}"/>'
    )


def render_svg(rows, counts, user, today, theme):
    """Draw one row per organization: logo, name, what the fix did, and its status."""
    out = [
        f'<g class="fade"><text class="m" x="{LEFT}" y="60" fill="{theme["muted"]}">'
        f'<tspan fill="{theme["accent"]}">$</tspan> gh search prs --author {user}</text>'
        f'<text class="m" x="{RIGHT}" y="60" text-anchor="end" fill="{theme["muted"]}">{today}</text></g>',
        f'<rect x="{LEFT}" y="84" width="{RIGHT - LEFT}" height="1" fill="{theme["rule"]}"/>',
    ]
    top = 84
    for index, row in enumerate(rows):
        lines = wrap(row["says"], "body", SAYS_SIZE, SAYS_WIDTH)
        first = top + 48
        refs_y = first + 28 * len(lines)
        height = refs_y - top + 30
        middle = top + height / 2
        name_size = min(NAME_SIZE, NAME_SIZE * (SAYS_X - 24 - NAME_X) / text_width(row["name"], "display", NAME_SIZE))
        tag, tag_fill = ("MERGED", theme["accent"]) if row["merged"] else ("IN REVIEW", theme["muted"])
        says = "".join(
            f'<text class="b" x="{SAYS_X}" y="{first + 28 * i}" fill="{theme["ink"]}">{html.escape(line)}</text>'
            for i, line in enumerate(lines)
        )
        out.append(
            f'<g class="row" style="animation-delay:{150 + 90 * index}ms">'
            f"{logo_tile(row, index, LEFT, round(middle - TILE / 2), theme)}"
            f'<text class="d" x="{NAME_X}" y="{round(middle + name_size * 0.36)}" font-size="{name_size:.1f}" '
            f'fill="{theme["ink"]}">{html.escape(row["name"])}</text>'
            f"{says}"
            f'<text class="m" x="{SAYS_X}" y="{refs_y}" fill="{theme["muted"]}">'
            f'{html.escape(fit_refs(row["refs"], RIGHT - SAYS_X - TAG_WIDTH))}</text>'
            f'<text class="m tag" x="{RIGHT}" y="{refs_y}" text-anchor="end" fill="{tag_fill}">{tag}</text></g>'
        )
        top += height
        if index < len(rows) - 1:
            out.append(f'<rect x="{NAME_X}" y="{top}" width="{RIGHT - NAME_X}" height="1" fill="{theme["rule"]}"/>')
    out.append(f'<rect x="{LEFT}" y="{top}" width="{RIGHT - LEFT}" height="1" fill="{theme["rule"]}"/>')
    footer = top + 36
    out.append(
        f'<text class="m" x="{LEFT}" y="{footer}" fill="{theme["muted"]}">{counts["merged"]} merged   '
        f'{counts["open"]} in review   {counts["total"]} upstream pull requests</text>'
        f'<text class="m" x="{RIGHT}" y="{footer}" text-anchor="end" fill="{theme["muted"]}">full log below</text>'
    )
    height = footer + 30
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" '
        'role="img" aria-labelledby="title description">',
        '<title id="title">Open source pull requests</title>',
        f'<desc id="description">{html.escape(summary(rows))}</desc>',
        "<style>",
        font_face("Upstream Display", FONTS["display"]),
        font_face("Upstream Body", FONTS["body"]),
        font_face("Upstream Mono", FONTS["mono"]),
        '.d{font-family:"Upstream Display","Arial Narrow",sans-serif}',
        f'.b{{font-family:"Upstream Body",Arial,sans-serif;font-size:{SAYS_SIZE}px}}',
        f'.m{{font-family:"Upstream Mono",ui-monospace,monospace;font-size:{MONO_SIZE}px;white-space:pre}}',
        ".tag{font-size:13px;letter-spacing:1.6px}",
        ".row{animation:rise 480ms cubic-bezier(.16,1,.3,1) both}",
        ".fade{animation:fade 400ms ease-out both}",
        "@keyframes rise{from{opacity:0;transform:translateY(18px)}}",
        "@keyframes fade{from{opacity:0}}",
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}",
        "</style>",
        f'<rect x=".5" y=".5" width="{WIDTH - 1}" height="{height - 1}" rx="15" fill="{theme["bg"]}" '
        f'stroke="{theme["rule"]}"/>',
        *out,
        "</svg>",
        "",
    ])


def summary(rows):
    def describe(group):
        return " ".join(f"{row['name']}: {row['says']} Pull requests: {', '.join(row['refs'])}." for row in group)

    merged = describe([row for row in rows if row["merged"]])
    review = describe([row for row in rows if not row["merged"]])
    return f"Merged upstream. {merged} In review. {review}"


def cell(text):
    return html.escape(text, quote=False).replace("|", "\\|")


def log_table(prs, config):
    rows = sorted(prs, key=lambda pr: (STATUS_ORDER[pr["status"]], pr["repo"].lower(), -pr["number"]))
    lines = ["| Status | Repository | Pull request |", "| :--- | :--- | :--- |"]
    lines += [
        f"| {status_label(pr, config)} | {pr['repo']} | [#{pr['number']}]({pr['url']}) {cell(pr['title'])} |"
        for pr in rows
    ]
    return lines


def readme_section(prs, config, rows):
    user = config["user"]
    upstream = [pr for pr in prs if not pr["repo"].startswith(f"{user}/")]
    own = [pr for pr in prs if pr["repo"].startswith(f"{user}/")]
    raw = f"https://raw.githubusercontent.com/{user}/{user}/main/assets"
    search = f"https://github.com/search?q=is%3Apr+author%3A{user}+is%3Apublic&type=pullrequests"
    return "\n".join([
        START,
        "## Open source",
        "",
        f'<a href="{search}">',
        "  <picture>",
        f'    <source media="(prefers-color-scheme: dark)" srcset="{raw}/upstream-dark.svg">',
        f'    <img alt="{html.escape(summary(rows))}" src="{raw}/upstream-light.svg" width="100%">',
        "  </picture>",
        "</a>",
        "",
        "Mostly bug fixes in projects I actually use.",
        "",
        "<details>",
        f"<summary><b>Every upstream pull request</b> ({len(upstream)})</summary>",
        "",
        *log_table(upstream, config),
        "",
        "</details>",
        "",
        "<details>",
        f"<summary><b>Pull requests in my own repositories</b> ({len(own)})</summary>",
        "",
        *log_table(own, config),
        "",
        "</details>",
        "",
        "<sub>Rebuilt daily from the GitHub API by <a href=\"upstream.py\">upstream.py</a>. Merges GitHub does not "
        "record, such as Copybara imports, are listed in <a href=\"upstream.json\">upstream.json</a>.</sub>",
        END,
    ])


def build(prs, config, today):
    """Write both images and return the README with the open source section replaced."""
    for pr in prs:
        pr["status"] = status(pr, config)
    rows = organization_rows(prs, config)
    upstream = [pr for pr in prs if not pr["repo"].startswith(f"{config['user']}/")]
    counts = {
        "merged": sum(pr["status"] in ("merged", "landed") for pr in upstream),
        "open": sum(pr["status"] == "open" for pr in upstream),
        "total": len(upstream),
    }
    for name, theme in THEMES.items():
        svg = render_svg(rows, counts, config["user"], today, theme)
        (ASSETS / f"upstream-{name}.svg").write_text(svg, encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    head, rest = readme.split(START, 1)
    tail = rest.split(END, 1)[1]
    return head + readme_section(prs, config, rows) + tail


if __name__ == "__main__":
    config = json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))
    prs = fetch_pull_requests(config["user"], os.environ["ACCESS_TOKEN"])
    readme = build(prs, config, datetime.date.today().isoformat())
    README.write_text(readme, encoding="utf-8")
