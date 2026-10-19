"""Generate theme-aware profile artwork from public GitHub data. Python stdlib only."""
import argparse
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USER = "priy-anshugupta"
THEMES = {
    "dark": ("#0d1117", "#161b22", "#30363d", "#e6edf3", "#919ba8", "#70cbbb"),
    "light": ("#ffffff", "#f6f8fa", "#d0d7de", "#1f2328", "#59636e", "#147d70"),
}


def fetch(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-artwork"}
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    with urlopen(Request("https://api.github.com" + path, headers=headers), timeout=30) as response:
        return json.load(response)


def shorten(value, limit=65):
    return value if len(value) <= limit else value[:limit - 1] + "…"


def activity_rows(events):
    rows = []
    seen = set()
    verbs = {"PushEvent": "pushed to", "PullRequestEvent": "pull request in",
             "IssuesEvent": "issue in", "ReleaseEvent": "release in",
             "CreateEvent": "created in", "PullRequestReviewEvent": "reviewed"}
    for event in events:
        kind = event.get("type")
        repo = event.get("repo", {}).get("name", "")
        # Exclude this profile's generated commits and passive star/fork activity.
        if kind not in verbs or repo == f"{USER}/{USER}":
            continue
        date = event.get("created_at", "")[:10]
        key = (kind, repo, date)
        if key in seen:
            continue
        seen.add(key)
        label = f"{date}  {verbs[kind]} {repo.removeprefix(USER + '/')}"
        rows.append(shorten(label))
        if len(rows) == 3:
            break
    return rows


def svg_start(width, height, title, description):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>')


def header(theme):
    from profile_artwork import header as draw_header
    return draw_header(theme)


def terminal(theme, profile, events, stamp):
    from profile_artwork import terminal as draw_terminal
    return draw_terminal(theme, profile, events, stamp, activity_rows(events))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, help="Use a local JSON fixture instead of GitHub")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9-]+", USER):
        raise ValueError("Invalid GitHub username")
    if args.fixture:
        data = json.loads(args.fixture.read_text(encoding="utf-8"))
        profile, events = data["profile"], data["events"]
    else:
        # Fetch everything before writing: a failed API request preserves the last good assets.
        profile = fetch(f"/users/{USER}")
        events = fetch(f"/users/{USER}/events/public?per_page=100")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    assets = ROOT / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        for name, value in (("header", header(theme)), ("activity", terminal(theme, profile, events, stamp))):
            (assets / f"{name}-{theme}.svg").write_text(value, encoding="utf-8")
    from profile_artwork import extra_assets
    for name, value in extra_assets().items():
        (assets / name).write_text(value, encoding="utf-8")
    print("Generated editorial header, contact cards, project cards and public-activity terminal.")


if __name__ == "__main__":
    main()
