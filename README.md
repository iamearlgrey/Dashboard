# Family Dashboard — image renderer

Renders a 7-day meal-plan + calendar + weather dashboard as a single
PNG, sized for an e-ink panel. An ESP32 fetches that PNG and draws it
— no app on the device, all the logic lives here.

## Where does "formatting" live?

Three separate concerns, three separate files:

| Concern | File | What it controls |
|---|---|---|
| **Data** | `fetch_calendar.py`, `fetch_weather.py`, `demo_data.py` | *what* the content is — event titles, times, temps |
| **Structure** | `models.py` | the shape data is passed around in (`Day`, `Event`, `DayWeather`) |
| **Formatting/layout** | `template.html` | *how it looks* — fonts, sizes, colors, spacing, grid — this is the file to edit for visual tweaks |
| **Wiring** | `render.py` | fills `template.html` with data and screenshots it to PNG — you shouldn't need to touch this for style changes |

This is genuinely just an HTML/CSS file (with Jinja2 `{{ }}` placeholders
where data gets inserted) rendered to a PNG by a headless browser
(Playwright). Open `template.html` in any text editor — the `<style>`
block at the top is exactly like editing CSS on a webpage. Change a
font-size, a color, a width, rerun `python3 main.py --demo`, and see
the result immediately. No Python knowledge needed for most tweaks.

One e-ink-specific gotcha worth knowing: avoid gray text (like
`color: #888`) for "de-emphasized" content. E-ink displays are pure
black/white, so anything gray gets thresholded into a speckly mess
instead of a clean color. Use `font-style: italic` or a smaller
`font-size` for de-emphasis instead — both survive the black/white
conversion cleanly.

## Files

```
config.py              # <-- edit this: your calendar feed URLs, location, display size
template.html            # <-- edit this: layout, fonts, sizes, colors (it's just HTML/CSS)
models.py                  # data shapes (Day, Event, DayWeather)
demo_data.py                 # fake data for testing without live feeds
fetch_calendar.py              # pulls + normalizes events from ICS feed URLs
fetch_weather.py                 # pulls high/low from Open-Meteo (free, no key)
render.py                          # fills template.html with data, screenshots to PNG
main.py                              # entry point — run this
fonts/                                  # bundled fonts (Poppins, Liberation Sans)
example_github_workflow.yml               # optional: run this on a free schedule, no home server
```

## Try it now

```bash
pip install -r requirements.txt
playwright install chromium   # one-time: downloads a headless browser (~150MB)
python3 main.py --demo
```

Writes `dashboard.png` with placeholder meals/events/weather so you
can see and tweak the layout immediately. The `playwright install`
step only needs to run once ever, not before every render.

## Wiring up real data

Calendar feed URLs are secrets (anyone with the link can read that
calendar), so they don't live in `config.py` — they live in a `.env`
file locally, and a GitHub Secret when this runs on a schedule.

1. **Meals calendar**: make a Google Calendar called "Meals," add
   all-day events for each day's dinner. Settings → that calendar →
   *Integrate calendar* → *Secret address in iCal format* → copy the URL.
2. **Family members' calendars**: same steps, one per person (or per
   shared calendar you want included).
3. Copy `.env.example` to `.env` (this file is gitignored — it will
   never get committed or pushed):
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and replace the placeholder JSON with your real feeds:
   ```
   CALENDAR_FEEDS_JSON=[{"name":"Meals","url":"https://calendar.google.com/.../basic.ics","color":"#000000","kind":"meal"},{"name":"Papa","url":"https://calendar.google.com/.../basic.ics","color":"#000000","kind":"event"}]
   ```
   It has to be valid JSON on one line — a list of objects, each with
   `name`, `url`, `color`, and `kind` (`"meal"` or `"event"`).
5. Also set `WEATHER_LATITUDE` / `WEATHER_LONGITUDE` in `.env` to your location.
6. Run `python3 main.py` (no `--demo`) — it'll pull live data.

iCloud and Outlook calendars also publish ICS URLs (iCloud: calendar
→ share → public calendar; Outlook: calendar settings → publish a
calendar → ICS link) — same JSON format works for those too.

## Putting the same secret on GitHub

Once you're happy with real data locally, the scheduled workflow
needs the same JSON, stored as an encrypted GitHub Secret instead of
a local file:

1. On your repo's GitHub page: Settings → Secrets and variables →
   Actions → New repository secret.
2. Name: `CALENDAR_FEEDS_JSON`
3. Value: paste the exact same JSON string from your `.env` file (just
   the value, not the `CALENDAR_FEEDS_JSON=` part).
4. Save. The workflow file already references
   `${{ secrets.CALENDAR_FEEDS_JSON }}` — nothing else to change.

This means your repo's actual code (including `.env.example`) is safe
to make public if you ever want to — the real URLs only exist in your
local `.env` (gitignored) and in GitHub's encrypted secret store, never
in a file that gets committed.

## Running it on a schedule without a home server

You don't need a Pi or an always-on machine. `example_github_workflow.yml`
(move it to `.github/workflows/render.yml` in your repo) runs `main.py`
every 30 minutes on GitHub Actions' free tier and commits the resulting
`dashboard.png` back to the repo, using the `CALENDAR_FEEDS_JSON` secret
you set up above — your real URLs never appear in the repo itself. Your
ESP32 then just fetches:

```
https://raw.githubusercontent.com/<you>/<repo>/main/dashboard.png
```

on wake, draws it, and goes back to sleep. Zero cost, zero maintenance.
Because the secrets live outside the repo, the repo can safely be
public or private — your choice.

## Next: the ESP32 side

Once you're happy with the layout, the firmware side is short:
wake on timer → HTTP GET the PNG (or a pre-converted raw bitmap) →
push to the panel via GxEPD2 → deep sleep. I can write that sketch
next once you've picked a specific display panel (let me know the
Waveshare model/size you land on — pinout and init code differ
slightly per panel).
