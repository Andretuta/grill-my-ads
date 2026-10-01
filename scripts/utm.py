#!/usr/bin/env python3
"""Append the standard Meta UTM template to a destination URL (keeps existing params). Stdlib only.

  utm.py https://example.com/offer
  utm.py https://example.com/offer?ref=x --source instagram
  utm.py --selftest
"""
import argparse
import sys
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

TEMPLATE = [
    ("utm_source", "facebook"), ("utm_medium", "paid_social"),
    ("utm_campaign", "{{campaign.name}}"), ("utm_term", "{{adset.name}}"),
    ("utm_content", "{{ad.name}}"), ("utm_id", "{{campaign.id}}"), ("placement", "{{placement}}"),
]


def build(url, source="facebook"):
    if "://" not in url:
        url = "https://" + url
    parts = urlsplit(url)
    q = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not k.startswith("utm_") and k != "placement"]
    q += [(k, source if k == "utm_source" else v) for k, v in TEMPLATE]
    # keep {{ }} macros readable: Meta replaces them at delivery
    query = urlencode(q, safe="{}.")
    return urlunsplit((parts.scheme, parts.netloc, parts.path or "/", query, parts.fragment))


def selftest():
    u = build("example.com/offer?ref=x&utm_source=old")
    assert u.startswith("https://example.com/offer?ref=x&utm_source=facebook&utm_medium=paid_social"), u
    assert "utm_content={{ad.name}}" in u and "old" not in u
    print("utm.py selftest OK")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        return selftest()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("url"); p.add_argument("--source", default="facebook")
    a = p.parse_args()
    print(build(a.url, a.source))


if __name__ == "__main__":
    main()
