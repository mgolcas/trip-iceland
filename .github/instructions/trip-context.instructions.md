---
description: "Use when working with the Iceland 2026 trip KML files or Dienu_Planas.txt. Provides project context, file conventions, and trip-specific data for the Iceland south-coast 5-day road trip."
applyTo: ["*.kml", "Dienu_Planas.txt", "Keliones_Asistentas.txt", "*.py"]
---

# Iceland 2026 Trip – Project Context

## Trip Summary
- **Dates**: 2026.09.07 – 2026.09.11 (5 days), 3 travellers
- **Route**: south coast by rented car (Ring Road / Kelias 1, paved — no 4x4/F-roads needed)
- **Flights**: 09.07 15:25 Vilnius (VNO) → 16:45 KEF (Keflavík) · 09.11 17:45 KEF → 09.12 00:40 Vilnius (VNO)
- **Car**: Zero Car — Dacia Duster 4WD (or class analogue), manual gearbox; reservation 09.07 17:00–09.11 17:00,
  picked up at KEF ~17:35 (after baggage), returned ~14:00–14:15 before the 17:45 flight
- **Lodging**: D01 (09.07–09.08) Gesthús Selfoss, Engjavegur 56, 800 Selfoss · D02–D04 (09.08–09.11)
  Farmhouse Lodge (Airbnb, host Arnar), Skeiðflöt 871 (near Vík), GPS `63.4374645, -19.1899663`
- **GitHub**: https://github.com/mgolcas/trip-iceland.git (branch: `main`)

## Key Files
| File | Purpose | Who reads it |
|------|---------|--------------|
| `Iceland.kml` | Day-route map — 5 layers (D01–D05), drive/walk lines. **Auto-generated** — never hand-edit | On-the-road daily navigation |
| `Dienu_Planas.txt` | **Master** human-readable itinerary with real clock times. Reread many times per day during the trip | Quick daily overview |
| `Keliones_Asistentas.txt` | Prep checklist + logistics (flights, car rental, fuel, documents, packing, food, safety, budget, restaurant links) | Pre-trip prep, occasional lookups |
| `tools/gen_day_maps.py` | Source of truth — DAYS/SEARCH/LINKS → generates `Iceland.kml` | Editing stops/coords |

**Rule**: `Dienu_Planas.txt` is the master reference for times and day numbering. `Iceland.kml` is always regenerated from `gen_day_maps.py` — never modified directly.

**Shared policy**: this file holds trip-specific baseline facts only. Cross-agent behavior (mandatory live
verification, source recording, KML/coordinate rigor, file-consistency rules) lives in
[`.github/instructions/trip-planner-shared.instructions.md`](trip-planner-shared.instructions.md), enforced
identically by the GitHub Copilot agent ([`.github/agents/trip-planner.agent.md`](../agents/trip-planner.agent.md))
and the Codex skill ([`.agents/skills/trip-planner/SKILL.md`](../../.agents/skills/trip-planner/SKILL.md)).

## Privatumas
Niekada failuose nesaugoti ir atsakymuose nekartoti rezervacijų kodų (PNR), PIN, bilietų numerių ar kitų
prisijungimo duomenų. Jei tokia informacija pateikta ekrano kopijoje ar laiške, ją užmaskuoti ir naudoti
tik neidentifikuojančią kelionės informaciją.

---

## Day Schedule Overview

| Day | Date | Weekday | Theme |
|-----|------|---------|-------|
| 01 | 09.07 | Pirmadienis | Vakarinis atvykimas KEF → Gesthús Selfoss |
| 02 | 09.08 | Antradienis | Auksinis ratas + kriokliai (Þingvellir, Geysir, Gullfoss, Kerið, Seljalandsfoss, Gljúfrabúi, Kvernufoss) ⚠️ INTENSYVI DIENA (~5h40 vairavimo, patikrinta OSRM 2026-08-19) |
| 03 | 09.09 | Trečiadienis | Waterfall Way žygis + Sólheimajökull + Katla ledo urvas 14:00 + Reynisfjara + Dyrhólaey |
| 04 | 09.10 | Ketvirtadienis | Fjaðrárgljúfur + Skaftafell (Svartifoss) + Diamond Beach + Jökulsárlón Zodiac 15:10 ⚠️ ILGA DIENA |
| 05 | 09.11 | Penktadienis | Reykjavík (Hallgrímskirkja, Sun Voyager) + Sky Lagoon 11:00 + auto grąžinimas + išvykimas 17:45 |

---

## Transport in Iceland

- **Car rental**: Zero Car / Blue Car keybox at KEF, ~3–4 min walk through P1 from the terminal. Complete
  Zero Car's online check-in before arrival for a faster handover (`patikrinta 2026-08-19`;
  zerocar.is/info/pickup-dropoff-process). Photograph the car (all sides, glass, tyres, fuel level) before
  departure; return with a full tank. Insurance already includes CDW + SCDW, Gravel Protection (GP), Sand &
  Ash Protection (SAAP), and Zero Excess.
- **Fuel**: self-service at N1, Olís, ÓB, Orkan, Atlantsolía — needs a card with PIN. Fill up at Hvolsvöllur,
  Vík, or Kirkjubæjarklaustur; fewer stations further along the route.
- **Roads**: paved Ring Road (Route 1) only for this plan — **no F-roads / no 4x4 requirement**. 4WD only
  helps traction on gravel/wet surfaces; it does not authorize closed roads or off-road driving. Do not
  continue past Fjaðrárgljúfur toward Laki / F206.
- **Parking**: see `Keliones_Asistentas.txt` section 6 for the per-day paid/free parking list with map links.

---

## Booking Requirements ⚠️

| Attraction | Booking needed? | Notes |
|------------|-----------------|-------|
| **Katla Ice Cave** | **BOOKED – D03 09.09 14:00–17:00** | Tröll Expeditions Super Jeep tour, 3 passengers, €631,38 total (`patikrinta 2026-07-06`). Meeting point: Vík-Inn hotel lobby, Víkubraut 26, 301 Vík; be ready by 13:40. |
| **Jökulsárlón Zodiac** | **BOOKED – D04 09.10 15:10** | Rescheduled from 09.06; 49 800 ISK / €349,42 total (`patikrinta 2026-07-06`; operator confirms Zodiac season May–Oct and current 2026 adult price 16 600 ISK/person — matches the booked rate, `patikrinta 2026-08-19`, icelagoon.is). Vatnajökull NP parking ~1 000 ISK, paid at the on-site kiosk. Check in at the ticket office 30 min before departure. |
| **Sky Lagoon (Saman ritual)** | **BOOKED – D05 09.11 11:00** | 3 adults, 50 970 ISK, paid in full — 0 ISK due on arrival (`patikrinta 2026-07-06`; still operating with a Saman package `patikrinta 2026-08-19`, skylagoon.com). |
| **Kerið crater** | Pay on arrival | ~600 ISK/person entry, includes parking (ticketed via kerid.is; exact current ISK figure not re-confirmed live on 2026-08-19 — recheck before travel). |
| **Sólheimajökull glacier walk / Skaftafell** | Self-guided stop, no booking | Do not walk onto the glacier unguided; Svartifoss/Skaftafell visitor center is a free self-guided stop. |

Unless a later item-specific date is shown, prices above were checked on **2026-07-06**. Recheck all of them
shortly before the trip per the shared verification policy.

---

## Iceland-Specific Notes

### Access & seasonal notes
- Nearly all stops are outdoor nature sites (waterfalls, beaches, glaciers, canyons, Þingvellir, Geysir,
  Gullfoss, Kerið) open **24/7** with no weekday-dependent closures — weekday of visit does not constrain access.
- **Dyrhólaey** is sometimes closed to visitors during the bird nesting season — verify current status before D03.
- **Jökulsárlón boat tours** (amphibian + Zodiac) run seasonally (roughly Jun–Sep); September is near the end
  of the season, which is why advance booking was required.
- Katla and Sólheimajökull glacier terrain must only be accessed with a guided tour — never unguided.

### Public holidays
- Iceland has **no public holidays in September** (previous is Commerce Day, first Monday of August; next is
  Christmas) — recheck for the exact travel dates, but no closures are expected 09.07–09.11.

### Weather & safety
- Weather changes fast — check **vedur.is** (forecast, aurora) and **safetravel.is** (road/travel alerts)
  every morning, and **road.is** (Vegagerðin) for real-time road conditions.
- **Reynisfjara "sneaker waves"** are deadly — stay far from the water, never turn your back to the sea.
- Strong wind can rip car doors open — hold them firmly, park facing into the wind.
- Don't stop on the road to photograph — use designated parking areas only.
- Weak/no signal away from towns — carry an offline Google Maps download of South Iceland.

### Money & budget
- Restaurants: practical budget ~€18–30/main, soup ~€12–18, hot dog ~€4 (Iceland is expensive — no
  Michelin/luxury). Groceries at Bónus/Krónan are cheaper than restaurants for breakfast/dinner.
- Full budget breakdown (flights, lodging, car, activities, food, fuel, parking, contingency) is maintained
  in `Keliones_Asistentas.txt` section 10.

### Restaurants (see `Keliones_Asistentas.txt` section 7 for links/hours)
`[D01]` Geysir Glíma (Geysir Center) · `[D02]` Skógafoss Bistro Bar · `[D02–D04]` Suður-Vík (Vík) ·
`[D03]` Halldórskaffi (Vík) · `[D03]` Black Beach Restaurant (Reynisfjara) · `[D04]` Systrakaffi
(Kirkjubæjarklaustur) · `[D05]` Bæjarins Beztu (Reykjavík).

---

## `Iceland.kml` Structure (auto-generated)
`Iceland.kml` has **5 `<Folder>` layers**, one per day (D01–D05). Every stop is a tappable `<Placemark>`.
All days use the parking pattern: `🅿️ parkingas (drive)` → `Sight (walk)` → `🅿️ grįžimas (walk, False)`.
Edit via `tools/gen_day_maps.py` (DAYS/SEARCH/LINKS tables), then regenerate with `python3 tools/gen_day_maps.py`.

- KML coordinates are `LONGITUDE,LATITUDE,0` (longitude first — KML standard).
- Maps links use `?api=1&query=Place+Name` (ASCII landmark name → Google place card with Directions) — NOT
  raw `LAT,LON`. Spaces → `+`.
- `maps_link()` looks up `(round(lon,4), round(lat,4))` in `LINKS` (CID override) then `SEARCH` (query
  string). All `DAYS` coords must round to 4 dp to match dict keys.
- **Google My Maps limit: 10 layers per map.** `Iceland.kml` has 5 day-layers — well under the limit.
- Route lines: 🚗 drive = blue (`ffff0000`, OSRM road geometry), 🚶 walk/hike = green (`ff008000`).
- Pin colours (this trip's `KINDS`): `hotel`=green, `parking`=blue, `sight`=red, `beach`=yellow,
  `transit`=purple, `food`=orange. (The shared policy's full palette also defines `museum`, `mosque`,
  `viewpoint`, `market`, `spa` for other trips — add to `KINDS` first if a new kind is genuinely needed here.)

---

## Driving-Time Realism

Never guess drive times — verify each leg with OSRM (`http://router.project-osrm.org/route/v1/driving/lon1,lat1;lon2,lat2?overview=false`),
planning time = OSRM minutes × 1.15 rounded to 5 min, and always show distance. Flag a day `⚠️ ILGA DIENA` if
driving exceeds ~4 h.

Verified one-way legs (OSRM, `patikrinta 2026-08-19`, planning time = OSRM × 1.15 rounded to 5 min):
KEF→Selfoss ~1h40/95 km · Selfoss→Þingvellir ~1h/50 km · Þingvellir→Geysir ~1h10/60 km ·
Geysir→Gullfoss ~10 min/10 km · Gullfoss→Kerið ~55 min/54 km · Kerið→Seljalandsfoss (via Selfoss) ~1h30/85 km ·
Seljalandsfoss→Kvernufoss ~35 min/31 km · Kvernufoss→Skeiðflöt ~20 min/21 km · Skeiðflöt→Skógafoss ~20 min/20 km ·
Skógafoss→Sólheimajökull ~20 min · Sólheimajökull→Vík ~32 min/31 km · Katla tour end→Reynisfjara ~15 min ·
Reynisfjara→Dyrhólaey ~20 min · Dyrhólaey→Skeiðflöt ~20 min · Skeiðflöt→Fjaðrárgljúfur ~1h25/83 km ·
Fjaðrárgljúfur→Skaftafell ~1h20/78 km · Skaftafell→Jökulsárlón ~1h/57 km · Jökulsárlón→Skeiðflöt ~3h25/207 km (D04 return) ·
Skeiðflöt→Reykjavík ~3h/172 km · Reykjavík→Sky Lagoon ~15 min/6 km · Sky Lagoon→KEF ~1h/44 km (incl. fuel stop).

D02 (~5h40 verified total, was estimated 5h50) and D04 (~7h incl. the Jökulsárlón return leg) are the two long
days — both flagged in `Dienu_Planas.txt`. The KEF→Selfoss and Selfoss→Þingvellir/Þingvellir→Geysir legs were
previously understated by 8-15 min each; `Dienu_Planas.txt` D01/D02 clock times were corrected accordingly on
2026-08-19 (D01 hotel arrival now aligned with the host-confirmed 21:00–22:00 window instead of an earlier,
OSRM-inconsistent 20:05).

---

## Weekday Names
Always **derive the weekday from the actual date** (compute it; never copy from a prior version).
Verified 2026: 09.07 Pirmadienis · 09.08 Antradienis · 09.09 Trečiadienis · 09.10 Ketvirtadienis ·
09.11 Penktadienis.

## Daylight (September, South Iceland)
Sunrise ~06:32–06:42, sunset ~20:05–20:19 across the trip dates (~13.5 h light). Plan outdoor stops to
finish before ~20:00. Display convention: keep this as a **single summary line in `Dienu_Planas.txt`'s
header block** (`☀️ ŠVIESA`) — do not repeat sunrise/sunset per day (avoids clutter).

---

## Verified GPS Coordinates
*(cross-checked, see `tools/gen_day_maps.py` `SEARCH`/`DAYS` for the authoritative current values;
recheck before finalising any change)*

| Stop | 🅿️ Parking (lon, lat) | Sight/object (lon, lat) |
|------|----------------------|-------------------------|
| Þingvellir P1 | `-21.13639, 64.25564` | Almannagjá `-21.1247, 64.2647` · Öxarárfoss `-21.1179, 64.2658` |
| Geysir | `-20.30337, 64.30927` | Strokkur `-20.3007, 64.3127` |
| Gullfoss | `-20.1299, 64.3252` | `-20.1199, 64.3271` |
| Kerið | `-20.8867, 64.0419` | `-20.8851, 64.0413` |
| Seljalandsfoss | `-19.9938, 63.6157` | `-19.9886, 63.6156` · Gljúfrabúi `-19.9864, 63.6209` |
| Skógafoss | `-19.5128, 63.5277` | Skógafoss `-19.5113, 63.5320` · Hestavaðsfoss `-19.5075, 63.5334` |
| Kvernufoss | `-19.49, 63.5251` | `-19.4814, 63.5288` |
| Sólheimajökull | `-19.3704, 63.5304` | `-19.3584, 63.5346` |
| Dyrhólaey | `-19.1289, 63.4041` | `-19.1284, 63.4015` |
| Reynisfjara | `-19.0447, 63.4042` | `-19.0716, 63.4057` |
| Fjaðrárgljúfur | `-18.1717, 63.7703` | `-18.1718, 63.7713` |
| Skaftafell VC | `-16.9665, 64.0165` | Svartifoss `-16.9753, 64.0275` |
| Jökulsárlón | `-16.17974, 64.04804` | `-16.1958, 64.0489` |
| Diamond Beach | `-16.1779, 64.0455` | `-16.1777, 64.0443` |
| Hallgrímskirkja P | `-21.92697, 64.1419` | Hallgrímskirkja `-21.92654, 64.14202` · Sun Voyager `-21.9224, 64.1475` |
| Sky Lagoon | — | `-21.94629, 64.11648` |

Other key points: KEF `-22.6056, 63.9850` · Gesthús Selfoss `-20.9875, 63.9329` ·
Skeiðflöt `-19.1899663, 63.4374645` · Hvolsvöllur `-20.2218, 63.7510` ·
Vík `-19.0061, 63.4186` · Vík-Inn hotel (Katla meeting point) `-19.0137, 63.4178`
