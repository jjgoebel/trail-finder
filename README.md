# Chicagoland First Rides

A one-page web app for finding beginner-friendly mountain bike trails around Chicago.

- **Map** of trailheads (Leaflet + OpenStreetMap). Tap **Show trail lines** to load the real trails live from OpenStreetMap.
- **Rideability guess** from live weather (Open-Meteo): rain over the last 48 h, freeze-thaw, and a 3-day forecast. It's a guess, so always tap the official status link (CAMBr Trailbot or the forest preserve).
- **Getting there**: parking, cost, facilities, plus Google/Apple/transit directions and distance from you.
- **Beginner filter** on by default.

## How to run it

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
```

Then visit http://localhost:8000. Location needs `localhost` or https, not a `file://` URL.

## Keeping it up to date

Trail facts live in `trails.js`. Each entry has a `verified` date and `sources`. To refresh, re-check the source pages, edit the entry, and bump `verified`. Live data (weather, trail lines) needs no edits.

## Data credits

Trail info: [CAMBr](https://cambr.org), Forest Preserve districts of Cook, DuPage and Will counties, Singletracks. Weather: [Open-Meteo](https://open-meteo.com). Map and trail lines: © OpenStreetMap contributors.
