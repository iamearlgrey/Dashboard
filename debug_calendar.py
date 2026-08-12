"""
Run this from inside your family-dashboard folder:
    python3 debug_calendar.py

It fetches your real feeds and prints exactly what it finds at each
step, so we can see where things are dropping out — a bad/missing
URL, a "kind" set wrong, or events outside this week's date range.
Doesn't print your feed URLs, only the results.
"""

from datetime import date, timedelta, datetime
from icalendar import Calendar
import recurring_ical_events
import requests

from config import CALENDAR_FEEDS
from localtime import today_local

today = today_local()
end = today + timedelta(days=7)

print(f"Today's date the script is using: {today}")
print(f"Looking for events between {today} and {end}")
print(f"Number of feeds found in CALENDAR_FEEDS_JSON: {len(CALENDAR_FEEDS)}")
print()

if not CALENDAR_FEEDS:
    print("!! CALENDAR_FEEDS is empty. That means CALENDAR_FEEDS_JSON in your")
    print("   .env either isn't set, is invalid JSON, or main.py isn't finding")
    print("   your .env file. Nothing further to check until this is non-empty.")

for feed in CALENDAR_FEEDS:
    name = feed.get("name", "(no name)")
    kind = feed.get("kind", "(no kind)")
    url = feed.get("url", "")
    print(f"--- Feed: {name}  (kind={kind}) ---")

    if not url or "xxx" in url or "yyy" in url:
        print("  !! This still looks like the placeholder URL from .env.example.")
        continue

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  !! Could not fetch this URL: {e}")
        continue

    try:
        cal = Calendar.from_ical(resp.text)
    except Exception as e:
        print(f"  !! Fetched something, but it doesn't look like valid ICS data: {e}")
        continue

    raw_vevents = [c for c in cal.walk() if c.name == "VEVENT"]
    print(f"  Raw VEVENT blocks in the whole feed: {len(raw_vevents)}")

    occurrences = recurring_ical_events.of(cal).between(today, end)
    print(f"  Occurrences landing in this week's window: {len(occurrences)}")
    for occ in occurrences:
        summary = str(occ.get("summary", "(untitled)"))
        dtstart = occ.get("dtstart").dt
        print(f"    - {dtstart}  {summary}")
    print()

print("Done.")
