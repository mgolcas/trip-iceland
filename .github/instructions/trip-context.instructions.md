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
| `Iceland.kml` | Thematic Google My Map — placemarks by theme + daily PLANAS folder | Quick map lookup |
| `Iceland_Dienos.kml` | Day-route map (1 day = 1 layer, drive/walk lines) | On-the-road daily navigation |
| `Dienu_Planas.txt` | Master human-readable itinerary with real clock times | Quick daily overview |
| `Keliones_Asistentas.txt` | Prep checklist + logistics (car, fuel, weather, safety) | Pre-trip prep |
| `tools/gen_day_maps.py` | Generator that builds the day-route map (OSRM driving geometry) | Regenerating the day map |

**Rule**: `Dienu_Planas.txt` is the master reference for times and day numbering. KML must match it.

## Day Schedule Overview

| Day | Date | Weekday | Theme |
|-----|------|---------|-------|
| 01 | 09.03 | Ketvirtadienis | Atvykimas + Auksinis ratas (Þingvellir, Geysir, Gullfoss, Kerið) |
| 02 | 09.04 | Penktadienis | Kriokliai + Waterfall Way hike (Seljalandsfoss, Skógafoss, Kvernufoss) |
| 03 | 09.05 | Šeštadienis | Sólheimajökull + Dyrhólaey + Reynisfjara |
| 04 | 09.06 | Sekmadienis | Jökulsárlón + Fjaðrárgljúfur + Diamond Beach ⚠️ ILGA DIENA |
| 05 | 09.07 | Pirmadienis | Reykjavík + auto grąžinimas + išvykimas |

## KML Folder Structure (`Iceland.kml`)
| # | Folder name | Purpose |
|---|-------------|---------|
| 1 | `1. Atvykimas / KEF / Reykjavík` | Airport + Reykjavík landmarks |
| 2 | `2. Auksinis ratas` | Golden Circle |
| 3 | `3. Kriokliai` | Waterfalls |
| 4 | `4. Pakrantė ir paplūdimiai` | Coast & beaches |
| 5 | `5. Ledynai ir kanjonai` | Glaciers & canyons |
| 6 | `6. Pėsčiųjų / žygio maršrutai` | Hiking routes (Waterfall Way) |
| 7 | `7. Restoranai` | Restaurants per day |
| 8 | `8. Nakvynės` | Lodging bases |
| 9 | `9. Dienos planas` | PLANAS [01]-[05] daily plan placemarks |

## KML Editing Rules
- Never hand-edit large KML as raw XML. Always write a Python script, run it, delete it.
- KML coordinates are `LONGITUDE,LATITUDE,0` (longitude first — KML standard).
- PLANAS / Maps links use `?api=1&query=LAT,LON` (latitude first in the *query* string).
- **Google My Maps limit: 10 layers per map.** `Iceland.kml` has 9 folders; the day-route
  map has 5 day-layers — both stay under the limit (single map each).

## Day-Route Map (preferred for navigation)
- `Iceland_Dienos.kml`: **1 day = 1 layer**; every stop is its own tappable placemark with its own `🔗`.
- Route lines: 🚗 drive = blue (`ffff0000`, follows roads via OSRM), 🚶 walk/hike = green (`ff008000`).
- Regenerate via `python3 tools/gen_day_maps.py` (edit its `DAYS` table first).

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
