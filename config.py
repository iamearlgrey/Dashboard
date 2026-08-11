"""
All the stuff you'll actually want to edit lives in this file:
  - display size
  - colors/fonts/spacing (the "theme")

Calendar feed URLs are NOT in this file anymore — they contain
"secret" links that work like passwords, so they live in a .env file
locally (never committed to git) and in GitHub Secrets when this runs
on a schedule. See .env.example for the format.
"""

import json
import os

from dotenv import load_dotenv

load_dotenv()  # reads .env if present; harmless no-op if it isn't (e.g. on GitHub Actions)

# ---------------------------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------------------------
# Waveshare 7.5" B&W e-paper is 800x480. Change this to match your panel.
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480

# e-ink panels are 1-bit (pure black/white, no gray) unless you have a
# grayscale panel. Keep this True for standard B&W e-paper.
DITHER_TO_1BIT = False

# ---------------------------------------------------------------------------
# DATA SOURCES
# ---------------------------------------------------------------------------
# Feed URLs come from the CALENDAR_FEEDS_JSON environment variable (set in
# .env locally, set as a GitHub Secret in CI) — see .env.example for the
# exact format. Nothing to edit here.
CALENDAR_FEEDS = json.loads(os.environ.get("CALENDAR_FEEDS_JSON", "[]"))

# Open-Meteo needs no API key, just a lat/lon. Defaults to Portland, OR.
# Not sensitive, fine to leave hardcoded here.
WEATHER_LATITUDE = float(os.environ.get("WEATHER_LATITUDE", "45.569692"))
WEATHER_LONGITUDE = float(os.environ.get("WEATHER_LONGITUDE", "-122.698162"))
TEMPERATURE_UNIT = "fahrenheit"  # or "celsius"
