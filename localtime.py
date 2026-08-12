"""
Figures out "today" using a fixed timezone (yours), not whatever
timezone the machine running this happens to be set to. That distinction
matters because this script runs in two very different places:

  - your Mac, which is correctly set to your local timezone
  - GitHub Actions, whose servers run on UTC — 7-8 hours ahead of
    Pacific time, so without this fix, the scheduled render would
    start showing "tomorrow" as today every evening, well before
    your actual day has turned over.

Using this everywhere "today" matters keeps both environments in sync.
"""

from datetime import date, datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover — only hit on Python < 3.9
    raise SystemExit(
        "This project needs Python 3.9 or newer (for the zoneinfo module). "
        "Run 'python3 --version' to check yours."
    )

from config import TIMEZONE


def today_local() -> date:
    return datetime.now(ZoneInfo(TIMEZONE)).date()
