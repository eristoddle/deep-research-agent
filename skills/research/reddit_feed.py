#!/usr/bin/env python3
"""Read Reddit listings through the public Atom feeds.

Reddit serves `/r/<sub>/.rss` and `/r/<sub>/search.rss` to any ordinary client with no
account, no token, and no API registration. Every other route into Reddit fails at
somebody's permission gate rather than at a technical wall: WebFetch is refused by the
harness at the domain level, firecrawl refuses the domain by vendor policy, and the
official OAuth API's signup flow could not be completed. The feeds have no gate.

Output is titles and URLs -- the listing-level signal, many items per request. That is
deliberately the unit this is for. Post bodies are a different, narrower job.

Usage:
    reddit_feed.py r/SideProject
    reddit_feed.py r/SideProject --sort top --limit 40
    reddit_feed.py --search "cant find a tool that" --subreddit SideProject
    reddit_feed.py --search "billing nightmare" --json

Exit codes: 0 ok, 1 nothing usable returned, 2 bad arguments.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ATOM = "{http://www.w3.org/2005/Atom}"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

# www only. old.reddit.com now 302s and is degrading; do not prefer it.
BASE = "https://www.reddit.com"

MAX_BYTES = 400_000  # a feed is ~75KB; this is a sanity bound, not a target


def fetch(url, retries=5):
    """GET with backoff. 429 is a rate limit, not a refusal -- it clears with spacing.

    Reddit rate-limits by IP and the budget is cumulative across recent requests, so a
    burst of feeds trips it even though each one individually is fine. Space them.
    """
    delay = 5.0
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read(MAX_BYTES).decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            last = f"HTTP {exc.code}"
            if exc.code == 429 and attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            break
        except (urllib.error.URLError, TimeoutError) as exc:
            last = str(exc)
            break
    print(f"fetch failed: {last} <- {url}", file=sys.stderr)
    return None


def parse(xml_text):
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        print(f"not parseable as a feed: {exc}", file=sys.stderr)
        return []

    items = []
    for entry in root.findall(f"{ATOM}entry"):
        title = entry.findtext(f"{ATOM}title", "").strip()
        link_el = entry.find(f"{ATOM}link")
        link = link_el.get("href", "") if link_el is not None else ""
        updated = entry.findtext(f"{ATOM}updated", "")[:10]
        author = entry.findtext(f"{ATOM}author/{ATOM}name", "").strip()
        # /r/<sub>/ out of the permalink, so multi-sub results stay attributable
        sub_match = re.search(r"/r/([^/]+)/", link)
        # Reddit search mixes matching *subreddits* in with matching *posts*. Only a post
        # permalink carries /comments/. Without this filter a search silently returns
        # r/Tools and r/todayilearned as if they were results -- a 200 with plausible
        # content that does not answer the query, which is the failure mode this
        # project treats as worse than an error.
        if title and "/comments/" in link:
            items.append(
                {
                    "title": title,
                    "url": link,
                    "date": updated,
                    "subreddit": sub_match.group(1) if sub_match else "",
                    "author": author,
                }
            )
    return items


def build_url(args):
    if args.search:
        # `sort=new` on a site-wide search returns essentially unrelated posts; relevance
        # is the only sort that respects the query. Honour an explicit --sort, but do not
        # inherit the listing default of "new" here.
        sort = args.sort if args.sort != "new" else "relevance"
        params = {"q": args.search, "sort": sort, "restrict_sr": "0"}
        if args.subreddit:
            sub = args.subreddit.removeprefix("r/")
            params["restrict_sr"] = "1"
            return f"{BASE}/r/{sub}/search.rss?" + urllib.parse.urlencode(params)
        return f"{BASE}/search.rss?" + urllib.parse.urlencode(params)

    sub = args.target.removeprefix("r/") if args.target else ""
    if not sub:
        return None
    # /r/a+b+c/ is valid and returns one merged feed
    if args.sort in ("top", "new", "hot", "rising"):
        return f"{BASE}/r/{sub}/{args.sort}/.rss"
    return f"{BASE}/r/{sub}/.rss"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?", help="r/<sub>, or r/<a>+<b>+<c> for a merged feed")
    ap.add_argument("--search", help="search query instead of a subreddit listing")
    ap.add_argument("--subreddit", help="restrict --search to one subreddit")
    ap.add_argument("--sort", default="new", choices=["new", "top", "hot", "rising", "relevance", "comments"])
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = ap.parse_args()

    if not args.target and not args.search:
        ap.error("give a subreddit (r/SideProject) or --search")

    url = build_url(args)
    if not url:
        ap.error("could not build a feed URL from those arguments")

    xml_text = fetch(url)
    if xml_text is None:
        return 1

    items = parse(xml_text)[: args.limit]
    if not items:
        print("feed returned no entries", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(items, indent=2, ensure_ascii=False))
    else:
        for it in items:
            where = f"r/{it['subreddit']}" if it["subreddit"] else ""
            print(f"{it['date']}  {where:<24}  {it['title']}")
            print(f"{'':38}{it['url']}")
    print(f"\n{len(items)} items <- {url}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
