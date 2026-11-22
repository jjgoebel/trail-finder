#!/usr/bin/env python3
"""Download current trail lines from OpenStreetMap for every trail in trails.js.

Writes trail-lines.json (compact) next to index.html. Re-run any time to refresh:
    python3 scripts/refresh_trail_lines.py
"""
import json, re, sys, time, subprocess, urllib.parse, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENDPOINTS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]
RADIUS_M = 2500

src = (ROOT / "trails.js").read_text()
trails = re.findall(r'id:\s*"([^"]+)".*?lat:\s*([-\d.]+),\s*lng:\s*([-\d.]+)', src, re.S)

out_path = ROOT / "trail-lines.json"
try:
    out = json.loads(out_path.read_text())
except Exception:
    out = {"trails": {}}


def query(lat, lng):
    q = (f'[out:json][timeout:60];way["highway"~"^(path|track|bridleway|cycleway)$"]'
         f'["bicycle"!="no"]["access"!~"^(private|no)$"](around:{RADIUS_M},{lat},{lng});out tags geom;')
    body = urllib.parse.urlencode({"data": q}).encode()
    for attempt in range(3):
        for ep in ENDPOINTS:
            try:
                # curl uses the system certificate store (python.org builds often lack one).
                r = subprocess.run(["curl", "-sS", "--fail", "-m", "180", "-A", "trail-finder/0.1",
                                    "--data-binary", "@-", ep], input=body, capture_output=True, check=True)
                return json.loads(r.stdout)
            except Exception as e:
                print(f"  {ep.split('/')[2]}: {e}", file=sys.stderr)
        time.sleep(10 * (attempt + 1))
    return None


only = set(sys.argv[1:])
for tid, lat, lng in trails:
    if only and tid not in only:
        continue
    print(f"{tid} …", flush=True)
    data = query(float(lat), float(lng))
    if not data:
        print("  failed, keeping previous data", flush=True)
        continue
    ways = []
    for w in data.get("elements", []):
        g = w.get("geometry")
        if not g:
            continue
        t = w.get("tags", {})
        surface = t.get("surface", "")
        dirt = bool(re.search(r"ground|dirt|earth|grass|mud|wood", surface)) or (not surface and t.get("highway") == "path")
        ways.append({
            "n": t.get("name", ""),
            "s": surface,
            "m": t.get("mtb:scale", ""),
            "d": 1 if dirt else 0,
            "c": [[round(p["lat"], 5), round(p["lon"], 5)] for p in g],
        })
    out["trails"][tid] = {"updated": datetime.date.today().isoformat(), "ways": ways}
    print(f"  {len(ways)} ways", flush=True)
    out_path.write_text(json.dumps(out, separators=(",", ":")))

print("done")
