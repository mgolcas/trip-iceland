---
description: "Use when working with the Iceland 2026 trip KML files or Dienu_Planas.txt. Provides project context, file conventions, and KML structure for the Iceland south-coast 5-day road trip."
applyTo: ["*.kml", "Dienu_Planas.txt", "*.py"]
---

# Iceland 2026 Trip – Project Context

## Trip Summary
- **Dates**: 2026.09.03 – 2026.09.07 (5 days), 3 travellers
- **Route**: south coast by rented car (Ring Road / Kelias 1, paved — no 4x4 needed)
- **Flights**: 09.03 06:35 Vilnius → 07:55 KEF · 09.07 17:25 KEF → 09.08 00:20 Vilnius
- **Car**: picked up at KEF (D01), returned at KEF (~14:30 on D05)
- **Lodging**: D01 Hvolsvöllur · D02–D04 Vík í Mýrdal
- **GitHub**: https://github.com/mgolcas/trip-iceland.git (branch: `main`)

## Key Files
| File | Purpose | Who reads it |
|------|---------|--------------|
| `Iceland.kml` | Day-route map — 5 layers (D01–D05), drive/walk lines. **Auto-generated** — never hand-edit | On-the-road daily navigation |
| `Dienu_Planas.txt` | Master human-readable itinerary with real clock times | Quick daily overview |
| `Keliones_Asistentas.txt` | Prep checklist + logistics (car, fuel, weather, safety, restaurant links) | Pre-trip prep |
| `tools/gen_day_maps.py` | Source of truth — DAYS/SEARCH/LINKS → generates `Iceland.kml` | Editing stops/coords |

**Rule**: `Dienu_Planas.txt` is the master reference for times and day numbering. `Iceland.kml` is always regenerated from `gen_day_maps.py` — never modified directly.

## Day Schedule Overview

| Day | Date | Weekday | Theme |
|-----|------|---------|-------|
| 01 | 09.03 | Ketvirtadienis | Atvykimas + Auksinis ratas (Þingvellir, Geysir, Gullfoss, Kerið) |
| 02 | 09.04 | Penktadienis | Kriokliai + Waterfall Way hike (Seljalandsfoss, Skógafoss, Kvernufoss) |
| 03 | 09.05 | Šeštadienis | Sólheimajökull + Dyrhólaey + Reynisfjara |
| 04 | 09.06 | Sekmadienis | Jökulsárlón + Fjaðrárgljúfur + Diamond Beach ⚠️ ILGA DIENA |
| 05 | 09.07 | Pirmadienis | Reykjavík + auto grąžinimas + išvykimas |

## `Iceland.kml` Structure (auto-generated)
`Iceland.kml` has **5 `<Folder>` layers**, one per day (D01–D05). Every stop is a tappable `<Placemark>`.
All days use the parking pattern: `🅿️ parkingas (drive)` → `Sight (walk)` → `🅿️ grįžimas (walk, False)`.
Edit via `tools/gen_day_maps.py` (DAYS/SEARCH/LINKS tables), then regenerate.

## KML Editing Rules
- `Iceland.kml` is **auto-generated** — never hand-edit. Always modify `tools/gen_day_maps.py` and run `python3 tools/gen_day_maps.py`.
- KML coordinates are `LONGITUDE,LATITUDE,0` (longitude first — KML standard).
- Maps links use `?api=1&query=Place+Name` (ASCII landmark name → Google place card with Directions) — NOT raw `LAT,LON`. Spaces → `+`.
- `maps_link()` looks up `(round(lon,4), round(lat,4))` in `LINKS` (CID override) then `SEARCH` (query string). All `DAYS` coords must round to 4 dp to match dict keys.
- **Google My Maps limit: 10 layers per map.** `Iceland.kml` has 5 day-layers — well under the limit.

## Day-Route Map — `Iceland.kml` (auto-generated)
- **1 day = 1 layer** (`<Folder>`); 5 days = 5 layers. Regenerate: `python3 tools/gen_day_maps.py`.
- Every stop is its own tappable `<Placemark>` with a Maps link. Route lines show the day visually — Google Maps does NOT turn-by-turn along a KML line.
- Route lines: 🚗 drive = blue (`ffff0000`, OSRM road geometry), 🚶 walk/hike = green (`ff008000`).
- **Each stop's coordinate = the OBJECT / viewpoint you actually visit.** Tap **Directions** for live nav.
- All days use `🅿️ parkingas (drive)` → `Sight (walk)` → `🅿️ grįžimas (walk, False)` pattern.
- Pin colours (KINDS): `hotel`=green, `parking`=blue, `sight`=red, `beach`=yellow, `transit`=purple.

## Driving-Time Realism
- Never guess drive times. Verify each leg with OSRM: `http://router.project-osrm.org/route/v1/driving/lon1,lat1;lon2,lat2?overview=false`.
- Planning time = OSRM minutes × 1.15, rounded to 5 min; always show distance, e.g. `(~3 val 15 min, 187 km)`.
- If a day's driving > ~4 h, flag it `⚠️ ILGA DIENA` (e.g. D04 Jökulsárlón ~6.5 h round trip from Vík).

## Weekday Names
- Always **derive the weekday from the actual date** (compute it; never copy from a prior version).
- Verified 2026: 09.03 Ketvirtadienis · 09.04 Penktadienis · 09.05 Šeštadienis · 09.06 Sekmadienis · 09.07 Pirmadienis.

## Iceland-Specific Notes
- Paved Ring Road only — **no 4x4 / F-roads** in this plan.
- Rental insurance must include **Gravel (GP)** and **Sand & Ash (SAAP)** protection.
- Fuel is self-service at N1/Olís/Orkan — needs a card with PIN; return car with a full tank.
- Safety: Reynisfjara **sneaker waves** are deadly; strong wind can rip car doors; weather
  changes fast — check vedur.is and safetravel.is daily.
- Budget food: groceries (Bónus/Krónan) + gas-station grills; mains ~€18-30, hot dog ~€4.

## Budget
- Restaurants: practical ~€18-30 per person (Iceland is expensive). No Michelin/luxury.
