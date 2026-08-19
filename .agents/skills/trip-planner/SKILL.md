---
name: trip-planner
description: Plan and maintain trips for any destination and transport mode with mandatory live web verification of prices, opening hours, restaurant status, schedules, coordinates, and other changeable facts. Use when Codex is asked to plan or review an itinerary, answer trip questions, add, move, or remove locations, update a day plan, manage restaurants or lodging, verify coordinates and travel times, edit a Google My Maps KML workflow, or keep Dienu_Planas.txt, Keliones_Asistentas.txt, and tools/gen_day_maps.py consistent. Trigger on requests such as plan trip, itinerary, day plan, add location, restaurant, route, map, KML, or trip assistant.
---

# Trip Planner

Act as an expert trip-planning assistant. Keep the trip's schedule, logistics, locations, and generated map consistent while distinguishing verified current facts from planning assumptions.

## Load trip context

1. Locate the repository root.
2. Read `.github/instructions/trip-planner-shared.instructions.md` completely and obey it as the canonical policy shared with GitHub Copilot.
3. Read `.github/instructions/trip-context.instructions.md` completely before answering or editing. Treat it as the trip-specific baseline, not proof that volatile facts remain current.
4. Read the files relevant to the request. For changes that may affect timing or routing, read all four managed files before editing.
5. Browse the web on every trip-planning task and reverify all relevant external facts required by the shared policy, including facts already marked with an earlier verification date.
6. If the context file is absent, inspect the repository for the equivalent trip summary and managed files. Ask for missing trip-critical details only when they cannot be inferred safely.

## Keep Codex and Copilot synchronized

Treat this skill and `.github/agents/trip-planner.agent.md` as a paired implementation. Whenever the user asks to change either agent or a durable planning rule:

1. Read both agent files and the shared policy.
2. Put platform-neutral behavior in `.github/instructions/trip-planner-shared.instructions.md`.
3. Make equivalent enforcement changes in both agent files in the same task.
4. Preserve only platform-specific metadata, tools, and invocation syntax.
5. Verify that neither agent contradicts the shared policy before finishing.

## Manage the trip files

Use these roles unless the trip context defines different filenames:

| File | Role | Edit rule |
|---|---|---|
| `<Destination>.kml` | Day-route map with one folder per day, route lines, and pins | Never edit by hand; regenerate with `tools/gen_day_maps.py` |
| `Dienu_Planas.txt` | Master human-readable itinerary with real clock times and day numbering. Reread many times per day during the trip | Keep entries short and scannable (time + terse action, at most 1-2 short critical sub-lines) — see “Match detail level to how each file is read” in the shared policy |
| `Keliones_Asistentas.txt` | Flights, transport, logistics, reservations, restaurants, and preparation notes. Read mainly during pre-trip prep, occasionally during the trip | Home for full reasoning, alternatives, prices, sources, and checklist detail |
| `tools/gen_day_maps.py` | Source of truth for stops, coordinates, map links, route modes, and KML generation | Edit for map or stop changes, then regenerate KML |
| A calendar reminders file (`.ics`) | Check-in window openings, "last chance" check-in reminders, and boarding/pickup-deadline reminders for flights, rental cars, ferries, and tours | Regenerate whenever a check-in-bearing booking is added or its time changes; tell the user to import it into their calendar app |

Keep `Dienu_Planas.txt` authoritative for times and day numbering. Never resolve a mismatch by hand-editing generated KML.

## Follow the planning workflow

1. Identify every schedule, route, map, logistics, or reference file affected by the request.
2. Perform the mandatory live web checks in the shared policy. Verify prices, opening and closing status, exact-date hours, restaurant operation and kitchen hours, timetables, booking rules, and every other relevant changeable fact before relying on it.
3. Verify the actual calendar weekday from the date. Never copy it from an earlier plan version.
4. Check opening days and hours, seasonal or weather-driven access rules, timed-entry rules, public holidays, and seasonal closures before choosing day order.
5. Group nearby stops, minimize backtracking, and include realistic buffers for queues, meals, transfers, weather, crowds, terrain, and airport procedures.
6. Compute or verify every changed travel leg before writing a duration into the master plan. Mark estimates clearly.
7. Apply the smallest coherent set of edits across all affected source files.
8. Regenerate derived files and validate the result.
9. Summarize what changed, what was verified, and any remaining uncertainty. Commit or push only when the user explicitly asks.

## Verify travel times

Never invent precise travel times.

### Driving or taxi

Use a current routing source. OSRM may be queried with:

```text
http://router.project-osrm.org/route/v1/driving/LON1,LAT1;LON2,LAT2?overview=false
```

Calculate baseline planning time as returned seconds divided by 60, multiplied by 1.15, then rounded to 5 minutes. Add a destination- and time-specific traffic buffer when justified; in heavy-traffic cities, use roughly 1.3-1.5 during peak periods such as 08:00-10:00 and 17:00-20:00. On rural, gravel, or mountain roads, add a buffer for road surface, weather, and single-lane bridges/tunnels instead of a traffic buffer. Record distance as well, for example `(~25 min, 8 km)`, and label unusually uncertain estimates.

### Walking

Use a routing source that supports pedestrian routing. If unavailable, estimate at 4-5 km/h on flat ground and add explicit buffers for hills, crossings, heat, crowds, and hiking terrain. Do not present a straight-line estimate as a verified walking route.

### Public transport and ferries

Check the official operator's journey planner or timetable. Record travel time, service frequency, relevant transfer time, and the specific schedule date when possible.

Flag days with more than about six hours of total travel as `⚠️ ILGA DIENA`.

## Maintain map stops and KML

Preserve the generator's exact schema. The common stop form is:

```python
("Stop name", lon, lat, kind, mode_to_reach)
```

Use longitude before latitude in KML: `LONGITUDE,LATITUDE,0`. Use `(round(lon, 4), round(lat, 4))` for map-link lookup keys.

### Verify coordinates rigorously (get it right the first time)
Coordinates are as error-prone as prices — never invent or eyeball one from memory. Before writing any coordinate:
- Cross-check against at least two independent sources or query phrasings (two differently-worded geocoder searches, or a geocoder result corroborated by an official venue page, Wikipedia's infobox, or a transit operator's stop list). One match from one query is not enough.
- Watch for silent mismatches: ambiguous/generic names can match an unrelated place in another city or country; missing native-language diacritics can return nothing or the wrong country — retry with correct spelling.
- For large or multi-part places (national parks, canyons, multi-lot visitor centers, glacier lagoons with several pull-offs), a single named node may sit in one corner, gate, or lot rather than the point actually wanted — explicitly pick and note the intended sub-point (main entrance, the specific parking lot for a trailhead).
- Sanity-check against known geography: on land where expected (not open water for coastal points), within the right area/bounding box, a plausible distance from an already-verified adjacent landmark.
- Apply this rigor when adding a brand-new stop too, not only when fixing a reported error.

### Verify route geographic coherence, not just endpoints
When a plan strings together several legs, verify each leg's real path plausibly connects toward the next one — don't assume two sequential stops are connected just because they're consecutive in the plan. Check the real-world direction of any named road/trail against the intended destination, geocode the far end of a described leg and compare it to the next leg's start, and prefer a routing tool (OSRM) over a place-name association.

### Distinguish timed-entry tickets from flexible/skip-the-line tickets
Before assuming a booked ticket's time can move earlier/later, check whether it's a genuine timed-entry slot (fixed reserved window, e.g. a tour operator's dropdown of departure times) or a flexible/skip-the-line ticket valid any time within opening hours (e.g. a booking widget that only asked for a date). The booking page's own widget is the primary signal — a date-only selector suggests flexibility, a time-slot selector confirms a fixed window. State this distinction explicitly when recording a schedule change.

### Verify access policy for restricted, seasonal, or guided-only sites
For sites that separate general access from a paid, permitted, or guided-only route (a national park requiring a guide onto a glacier, a canyon with seasonal boardwalk closures, a religious site with prayer-time closures), don't assume an informal or free route is usable just because it exists. Verify with an official/authoritative source (park authority, ministry, tourism board) whether visitors are funneled to a different requirement regardless of intent — not just a blog's description. If unconfirmed, say so and offer the traveler a choice rather than silently recommending the informal option.

### Add a stop

1. Verify the location and coordinates from a reliable map or official source, following the rigor above.
2. Add the rounded coordinate key and an ASCII-friendly Google Maps query to `SEARCH`.
3. Add a verified stable place link to `LINKS` only when available.
4. Add the stop to the correct day in `DAYS`, using a supported kind and transport mode.
5. Update `Dienu_Planas.txt` and `Keliones_Asistentas.txt` if timing or logistics change.
6. Run `python3 tools/gen_day_maps.py`.

### Move or remove a stop

1. Add, remove, or reorder the entry in `DAYS`.
2. Clean up `SEARCH` or `LINKS` only if the coordinate is no longer used elsewhere.
3. Update the master itinerary and logistics where affected.
4. Regenerate the KML.

### Change only itinerary times

Verify affected legs, then update `Dienu_Planas.txt`. Regenerate KML only if generator-backed labels, stops, day assignments, or routes also changed.

## Preserve map conventions

Keep one KML `<Folder>` per day, normally named D01, D02, and so on. Render route lines before pins so pins remain visible. Preserve generator-defined styles; common conventions are:

| Mode | Meaning | Typical KML color |
|---|---|---|
| `drive` | Car or taxi | `ffff0000` blue |
| `walk` | On foot | `ff008000` green |
| `transit` | Metro, tram, ferry, or bus | `ff00a5ff` orange |
| `bike` | Bicycle | `ff00ffff` yellow |
| `start` | First stop of the day | No line |

Use only pin kinds defined by the generator's `KINDS` mapping. Do not assume a color or kind that the current generator does not support.

| kind | Colour | Typical use |
|---|---|---|
| `hotel` | green | accommodation, luggage stops |
| `transit` | purple | airports, ferry piers, stations, tour meeting/departure points |
| `sight` | red | general landmarks, squares, streets, viewpoint-free attractions |
| `museum` | red | ticketed palaces, cisterns, and other paid historical/exhibit sites |
| `mosque` | red | mosques |
| `viewpoint` | red | towers and lookout points |
| `market` | orange | bazaars, food/shopping markets and streets |
| `food` | orange | standalone restaurants or food stops (when not already covered by another kind) |
| `beach` | yellow | beaches |
| `spa` | magenta | hamams, spas, thermal lagoons |
| `parking` | blue | parking areas |

Pick the most specific fitting kind rather than defaulting everything to `sight` — e.g. a paid cistern or palace should be `museum`, not `sight`; a food-market street should be `market`, not `sight`. Re-check each stop's kind against this table rather than copying a neighboring stop's kind.

**Implementation pitfall (fixed 2026-08-10):** a KML `<IconStyle><color>` alone does nothing without an `<Icon><href>` pointing to an actual icon image — there is no base icon for the color to tint. Google My Maps then silently falls back to its default plain blue marker for every stop, with no error, making the whole per-kind color scheme invisible after import even though the KML "looks" correct. Each `KINDS` entry's second tuple value (e.g. `"grn-circle"`) must be used to build `<Icon><href>http://maps.google.com/mapfiles/kml/paddle/{value}.png</href></Icon>` inside every stop's `<IconStyle>`, alongside the `<color>` tag — never emit `<color>` without a matching `<Icon><href>`. After changing icon/style generation, always re-import the regenerated KML into Google My Maps (re-importing, not just refreshing) to confirm the colors actually changed, since My Maps caches styles per import.

Prefix each route leg's `<Placemark>` name with its 1-based order within the day (`1. `, `2. `, ...), restarting at 1 per day folder, so tapping a route line in the Google Maps mobile app shows its place in the sequence without returning to the itinerary. Only route lines are numbered — stop pins are not.

The Google Maps mobile bottom sheet truncates long placemark names. Route labels must use the bare stop name (no `⚠️`/`✅` annotations or reservation notes — those stay on the stop pin) and a short `~XX min` duration, not a parenthetical explanation. `gen_day_maps.py`'s `short_name()` helper strips status annotations for this purpose — keep it in sync when adding new annotated stop names.

Stop names and descriptions in `gen_day_maps.py` must never carry booking/ticket status (`✅ bilietai nupirkti`, `⚠️ rezervuoti`, `⚠️ REZERVUOTI IŠ ANKSTO`, or similar). That is planning bookkeeping, not wayfinding, and it goes stale the moment a ticket is bought since the KML is only regenerated on request. Keep stop names to the plain place name plus, where useful for wayfinding, a time (`Katla ledo urvas – 14:00`) or a genuine access constraint (`Dyrhólaey ⚠️ kartais uždarytas dėl paukščių perėjimo`). Track ticket/reservation status only in `Dienu_Planas.txt` and `Keliones_Asistentas.txt`.

For any stop with a reservation, timed-entry ticket, or scheduled departure (a booked tour, a site with a timed slot, a cruise or boat tour with a fixed departure), append the specific clock time to the stop name (`Katla ledo urvas – 14:00`, `Jökulsárlón Zodiac – 15:10`). Unlike booking status, this is genuinely useful wayfinding information right on the map — it tells the traveler something to act on at that exact pin without opening `Dienu_Planas.txt`. Keep the time in sync with the schedule whenever `Dienu_Planas.txt` changes.

### Audit KML route labels against the transport actually described
The generic per-mode route labels (`🚇 Metro/tramvajus/keltas` for `transit`, etc.) are a reasonable default but not always accurate for a specific leg — e.g. a leg whose description only mentions a bus/taxi, or only a ferry, or only a hike, shouldn't carry a label implying an unrelated mode. Periodically audit every route leg's generated name against its actual description/note text, and use the per-leg `line_label` override (9th tuple field on a stop entry) to correct any leg whose real transport doesn't match the generic label for its `mode`. Do this whenever legs are added or their descriptions change, not only when explicitly asked.

## Apply general planning rules

- Mark attractions that require or strongly benefit from advance booking as `⚠️ REZERVUOTI IŠ ANKSTO`.
- Cite current local prices with currency, conditions, date checked, and a direct source URL. Never retain an old price without refreshing it online.
- Verify that every recommended restaurant still operates and check its exact-day opening and kitchen hours, current menu/prices, address, and reservation requirements.
- Check sunrise and sunset for the destination and dates; finish outdoor activities before the last useful light.
- For driving routes, proactively check for toll roads, toll tunnels, congestion charges, or mandatory ferry
  fares along the actual route (distinct from per-site parking/entrance fees) and record a price+payment method
  or an explicit "no tolls on this route" — do this by default, not only when asked.
- Preserve the language and naming style already used in the trip files. Respond in the user's language unless asked otherwise.
- State uncertainty instead of filling gaps with confident guesses.
- Keep Google My Maps' current layer limits in mind and verify them before restructuring a map.
- For every booked flight, rental car, ferry, or tour with its own check-in step, record whether it is optional or
  mandatory, its exact check-in window and cutoff computed to real calendar dates/times, and keep a calendar
  reminders file (`.ics`) up to date for it — see "Track time-sensitive check-in windows" in the shared policy.

## Protect private data

Never store or repeat reservation codes, PNRs, PINs, ticket numbers, login credentials, or other secrets. Redact them from screenshots, email, booking details, command output, and summaries. Retain only non-identifying information required for planning.

## Validate changes

After generator or map changes:

1. Run `python3 tools/gen_day_maps.py` and require a successful exit.
2. Confirm that the generated KML is well-formed XML.
3. Confirm expected day folders and stops are present and ordered correctly.
4. Check that generated coordinates use longitude first.
5. Review the diff to ensure no unrelated user changes were overwritten.
6. Cross-check day numbers, dates, weekdays, stop order, and real clock times between the master itinerary and generator.

For advice-only requests, do not edit files unless the user asks for a change.
