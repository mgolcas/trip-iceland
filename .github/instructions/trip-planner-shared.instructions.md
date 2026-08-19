---
description: "Mandatory shared policy for the Codex and GitHub Copilot trip-planner agents: live web verification, source recording, file consistency, and cross-agent synchronization."
applyTo: ["Dienu_Planas.txt", "Keliones_Asistentas.txt", "*.kml", "tools/gen_day_maps.py", ".github/agents/trip-planner.agent.md", ".agents/skills/trip-planner/SKILL.md"]
---

# Shared Trip Planner Policy

Treat this file as the canonical behavioral policy shared by:

- Codex: `.agents/skills/trip-planner/SKILL.md`
- GitHub Copilot: `.github/agents/trip-planner.agent.md`

Read this file completely before every trip-planning answer or edit.

## Always verify live information

Use the internet on every trip-planning task before relying on any external fact that can change. Recheck even when the repository already contains a value or a prior verification date. Reuse a result only within the same active task when it still answers the exact question.

Verify every relevant item that can reasonably be checked online, including:

- ticket, tour, service, restaurant, transport, card, taxi, toll, tax, and booking prices;
- currency, whether the amount is per person or total, what is included, and any extra fee;
- whether an attraction, restaurant, hotel, route, or service still operates;
- opening hours for the exact planned weekday and date, last admission, kitchen closing time, last seating, prayer closures, seasonal schedules, maintenance, private events, and public-holiday exceptions;
- reservation requirements, timed-entry rules, cancellation rules, age limits, dress rules, accessibility, accepted payment methods, and required documents;
- restaurant address, current name, official menu, meal-service hours, reservation policy, and recent operational status;
- transit route, transfer stations, timetable, frequency, journey time, disruptions, first/last service, ferry sailing time, and current fare;
- driving and walking route, distance, realistic duration, traffic, hills, closures, and verified coordinates;
- flight and airport information, baggage/check-in rules, terminal, airport transfer, and required arrival buffer;
- public holidays, visa/passport rules, health and safety guidance, emergency numbers, weather forecast, sunrise, and sunset.

Do not use model memory, an old plan, or an earlier verification date as proof that current information is still correct.

## Use reliable sources

Prefer sources in this order:

1. Official government, venue, attraction, transport operator, airport, airline, hotel, restaurant, or booking page.
2. Official verified social profile or current official menu/reservation system when the main site lacks the detail.
3. Current Google Maps business listing or a reputable booking platform for operational status and hours.
4. Reputable secondary sources only when primary sources are unavailable.

For restaurants, check the official website/menu or official social profile and corroborate operational status and the exact day's hours with a current map/business listing when possible. Do not infer that a restaurant is open merely because an old directory page exists.

For safety-critical, deadline-critical, legally material, or conflicting information, confirm with at least two current sources when possible. When sources conflict, prefer the authoritative primary source and disclose the conflict.

## Verify GPS coordinates rigorously

Coordinates are as error-prone and as important to verify as prices or opening hours. Never invent, estimate, or eyeball a coordinate from memory — look every stop up fresh, even when the file already has a value, and get it right the first time rather than waiting for the user to spot a misplaced pin on the rendered map.

- Cross-check every coordinate against at least two independent sources or query phrasings before treating it as verified (for example, two differently-worded geocoder searches, or a geocoder result corroborated by an official venue page, Wikipedia's infobox coordinates, or a transit operator's stop list). A single match from one query is not sufficient.
- Watch for silent mismatches: ambiguous or generic names (chain shops, common words) can match an unrelated place in another city or country; names without correct native-language diacritics can return nothing or a wrong-country result — retry with correct spelling.
- For large or multi-part places (bazaars, palace grounds, multi-pier ferry terminals, multi-entrance complexes, national parks), a single named node from a geocoder may sit in one corner, one gate, or one specific dock rather than the point actually wanted. Explicitly decide and note which sub-point is intended (main tourist entrance, the specific parking lot for a trailhead, etc.) instead of accepting whatever a search happens to return.
- Sanity-check the result against known geography before accepting it: is it on land where it should be (not in open water for a coastal/ferry point), within the expected neighborhood or bounding box, and a plausible distance from an adjacent already-verified landmark or transit stop? Do not accept a coordinate on faith just because a geocoder returned it.
- Apply this same rigor when adding a brand-new stop, not only when fixing a reported error.

## Verify that a planned route is geographically coherent, not just its endpoints

When a plan strings together several legs (walk here, then take transport X), verify that each leg's actual path plausibly connects toward the next one — do not assume two sequential stops are connected just because they appear consecutively in the plan. A concrete failure mode from a past trip: "walk from Taksim to Kabataş via Istiklal Street" was proposed, but Istiklal Street leads to Tünel Square, in the opposite direction from Kabataş — the two points are ~1.8 km apart in unrelated directions, so no such walk exists. Before finalizing a multi-leg route: (1) check the real-world direction/layout of any named street, trail, or road against the intended destination, not just its starting point; (2) if unsure, geocode the far end of a described leg and compare it to the next leg's starting point; (3) prefer verifying via a routing tool (OSRM walking/driving) over trusting a place-name association. Apply this whenever a route involves walking, driving, or transferring between named roads, trails, or interchanges.

## Distinguish timed-entry tickets from flexible/skip-the-line tickets before assuming a time can move

Before assuming a booked ticket's arrival time can be moved earlier or later, verify whether it is a genuine timed-entry slot (a specific reserved time window, like a dropdown of departure times) or a flexible/skip-the-line ticket valid any time within opening hours (a booking widget that only asks for a date, not a time). Check the booking page's own widget/flow as the primary signal — a date-only selector strongly suggests flexibility, a time-slot selector confirms a fixed window — and note this distinction explicitly when recording the change, since misreading a flexible ticket as fixed (or vice versa) can wrongly constrain or wrongly loosen a schedule.

## Verify tourist access policy, not just price, for religious/heritage/protected sites with restricted entrances

For sites that separate a general or worship entrance from a paid tourist/permit entrance, or that restrict access by season, weather, or booked slot (a national park visitor center, a glacier area requiring a guided tour, a religious site with prayer-time closures), do not assume a "free" or informal entrance is usable just because it exists and is free. Verify with an official or authoritative source (park authority, ministry/foundation announcement, official tourism-board notice) whether visitors are actually funneled to a different route or requirement regardless of intent, not only a general blog's description of what's available. When this cannot be confirmed with confidence, say so explicitly and offer the traveler a choice (pay/book for guaranteed entry, or risk it) rather than silently recommending the free or informal option as if it were confirmed to work.

## Identify toll roads and other route-wide charges by default

For any trip that involves driving (or a route with tunnels, bridges, ferries, or a city congestion zone), proactively check — without waiting to be asked — whether the planned route crosses any toll road, toll tunnel, congestion charge, or mandatory vehicle fare, as a check distinct from per-site parking and entrance fees (which are already tracked per day). For every leg of the route:

- identify each toll point by name and confirm whether the itinerary actually passes through it (a toll existing somewhere in the destination country does not mean this specific route uses it);
- record the price, vehicle-type/axle basis if it varies, and the payment method and deadline (electronic plate-based tolls in several countries, including Iceland's tunnel tolls, must be paid online within a set window after the crossing, not at a gate);
- if the route has no tolls at all, state that explicitly in `Keliones_Asistentas.txt` (e.g. alongside the parking table) rather than leaving the question unanswered — a confirmed "no tolls on this route" is as valuable as a toll list;
- do this automatically whenever a driving route is planned or changed, not only when the traveler asks about tolls.

## Audit KML route labels against the transport actually described

`tools/gen_day_maps.py`'s generic per-mode route labels (e.g. a `transit` label implying metro/tram/ferry) are a reasonable default but are not always accurate for a specific leg — e.g. a leg whose description only mentions a bus/taxi, or only a ferry, or only a hike, should not carry a label implying an unrelated mode. Periodically audit every route leg's generated name against its actual description/note text, and use the per-leg `line_label` override (9th tuple field on a stop entry, where supported) to correct any leg whose real transport doesn't match the generic label for its `mode`. Do this whenever legs are added or their descriptions change, not only when explicitly asked.

## Record verification

For every changed price, opening time, timetable, reservation rule, or similar volatile fact:

- record the value, currency, relevant conditions, and `patikrinta YYYY-MM-DD` in the appropriate trip file;
- retain a direct source URL near the fact or in the relevant reservation/reference section;
- distinguish a verified fact from an estimate;
- avoid false precision for future schedules that have not yet been published.

If live verification is unavailable, fails, or produces no reliable answer, mark the item `⚠️ NEPATVIRTINTA`, state what must be checked, and do not present it as current. Do not finalize a schedule that depends on an unverified opening time or departure.

For a future trip, verify again shortly before booking, 7–14 days before departure, and on the travel day for same-day variables such as disruptions, prayer times, weather, traffic, road/trail conditions, and ferry/transit service.

## Track time-sensitive check-in windows and create calendar reminders

Flights, rental cars, ferries, and some tours impose their own mandatory or time-limited check-in step that is
separate from the trip's own schedule and easy to miss because it falls before or between travel days. For every
booked flight, rental car, ferry, or tour that has one, verify and record in `Keliones_Asistentas.txt`:

- whether online/app check-in is optional or mandatory (e.g. some rental agencies have no on-site process at all
  and require a completed online check-in before their keybox/counter will release the booking);
- the exact window it becomes available (often relative to departure/pickup, e.g. "opens 48 hours before departure"
  or "7 days before pickup") and any earlier automatic check-in the traveler may have purchased;
- any hard cutoff (boarding-gate time, latest online check-in time, latest on-site arrival) and the fee or
  consequence of missing it;
- compute the actual calendar date/time for each window and cutoff from the trip's real booked times — never leave
  it as a relative rule the traveler has to recompute themselves under time pressure.

Whenever a new check-in-bearing booking is confirmed or its time changes, regenerate or update a calendar file
(`.ics`, one `VEVENT` per reminder, UTC `Z` timestamps so every device renders it correctly regardless of local
timezone) covering at least: each check-in window opening, a final "last chance to check in" reminder before the
window closes, and a boarding-gate/pickup-deadline reminder timed to give the traveler enough buffer to act (not
timed at the deadline itself). Tell the user the file was generated and that they still need to import it into
their calendar app — this repository cannot create the reminder for them automatically.

## Match detail level to how each file is read

`Dienu_Planas.txt` and `Keliones_Asistentas.txt` serve different reading patterns and must not duplicate the same detail:

- **`Dienu_Planas.txt`** is reread many times *before and during each specific day* to answer "what time, what next". Keep every entry short and scannable: one line per event (time + emoji + terse action), plus at most one or two short sub-lines only for information needed in that exact moment (a hard time constraint, a critical warning, a phrase to say, a short address). Never put verification sources, prices with citation dates, alternative options, or reasoning/background there — link or defer to `Keliones_Asistentas.txt` instead.
- **`Keliones_Asistentas.txt`** is read mainly once during final pre-trip prep, and only occasionally during the trip for lookups. It is the right home for preparation checklists, full logistics reasoning, alternatives considered and why one was chosen, verification sources/dates, prices, restaurant details/addresses, and any explanatory text.
- When a task adds verified detail (a price, a source, an alternative, a reasoning trail), write the full version into `Keliones_Asistentas.txt` (or `trip-context.instructions.md` for durable baseline facts) and surface only the minimal actionable line in `Dienu_Planas.txt`.
- When editing `Dienu_Planas.txt` for any reason, check whether it has accumulated verbose content that belongs in `Keliones_Asistentas.txt` and move it in the same task instead of leaving it duplicated.

## Number map routes for mobile use

Google My Maps on mobile shows only the tapped route segment's name, not its position in the day. To keep the order clear directly on the map, prefix every route (leg) `<Placemark>` name with its 1-based sequence number within that day's folder (for example `1. 🚶 Pėsčiomis (...): A → B`, `2. ...`), restarting at 1 for each day. Apply this whenever the KML generator builds route placemarks; do not number the stop pins themselves.

The Google Maps mobile app truncates long placemark names in its bottom-sheet preview. Keep each route name short: use the plain stop name without `⚠️`/`✅` status annotations or reservation notes (those belong on the stop pin itself, which has more display room), and keep duration text to a short `~XX min` form rather than a parenthetical explanation. Move any extra detail to the stop pin's description or to `Keliones_Asistentas.txt`.

## Keep booking-status text out of the KML

`tools/gen_day_maps.py` stop names and descriptions must never carry booking/ticket status (`✅ bilietai nupirkti`, `⚠️ rezervuoti`, `⚠️ REZERVUOTI IŠ ANKSTO`, or similar). That status is planning bookkeeping, not wayfinding information, and it drifts out of sync the moment a ticket is bought or a plan changes, since the KML is only regenerated on request rather than whenever such status changes. Keep stop names to the plain place name plus, where useful for wayfinding, a time (`Katla ledo urvas – 14:00`) or a genuine access constraint that affects when you can physically enter (`Dyrhólaey ⚠️ kartais uždarytas dėl paukščių perėjimo`). Track ticket/reservation status only in `Dienu_Planas.txt` (terse `✅ BILIETAI NUPIRKTI` marker on the schedule line) and `Keliones_Asistentas.txt` (full reservation details). When adding or updating a KML stop, check its name against this rule before regenerating.

## Show the required arrival time for reserved/timed-entry stops

For any stop with a reservation, timed-entry ticket, or scheduled departure (a booked tour, a site with a timed slot, a cruise or boat tour with a fixed departure), append the specific clock time to the stop name in `tools/gen_day_maps.py` (`Katla ledo urvas – 14:00`, `Jökulsárlón Zodiac – 15:10`). This is genuinely useful wayfinding information on the map itself — unlike booking status (see above), a required arrival time tells the traveler something they need to act on at that exact pin, right when they need it, without opening `Dienu_Planas.txt`. Keep the time in sync with the schedule whenever `Dienu_Planas.txt` changes.

## Categorize every stop by pin kind (icon color)

Every stop in `tools/gen_day_maps.py`'s `DAYS` list carries a `kind` that the generator maps to a pin color via its `KINDS` dict, so the map is visually scannable by type at a glance. The full reference palette (use only the kinds a given trip's `KINDS` dict actually defines — add a new one there first if genuinely needed):

| `kind` | Colour | Typical use |
|---|---|---|
| `hotel` | green | accommodation, luggage stops |
| `transit` | purple | airports, ferry piers, stations, tour meeting/departure points |
| `sight` | red | general landmarks, squares, viewpoints, natural attractions |
| `museum` | red | ticketed palaces, cisterns, and other paid historical/exhibit sites |
| `mosque` | red | mosques (or other single-purpose worship sites) |
| `viewpoint` | red | towers and lookout points |
| `market` | orange | bazaars, food/shopping markets and streets |
| `food` | orange | standalone restaurants or food stops (when not already covered by another kind) |
| `beach` | yellow | beaches, black-sand shores |
| `spa` | magenta | hamams, spas, thermal lagoons |
| `parking` | blue | parking areas |

Pick the most specific fitting `kind` rather than defaulting everything to `sight` — e.g. a paid cistern or palace should be `museum`, not `sight`; a food-market street should be `market`, not `sight`; a thermal lagoon should be `spa`, not `sight`. When adding or reviewing stops, re-check each one's `kind` against this table rather than copying whatever a neighboring stop used.

**Implementation pitfall (fixed 2026-08-10):** a KML `<IconStyle><color>` alone does nothing without an `<Icon><href>` pointing to an actual icon image — there is no base icon for the color to tint. Google My Maps then silently falls back to its default plain blue marker for every stop, with no error, making the whole per-kind color scheme invisible after import even though the KML "looks" correct. Each `KINDS` entry's second tuple value (e.g. `"grn-circle"`) must be used to build `<Icon><href>http://maps.google.com/mapfiles/kml/paddle/{value}.png</href></Icon>` inside every stop's `<IconStyle>`, alongside the `<color>` tag — never emit `<color>` without a matching `<Icon><href>`. After changing icon/style generation, always re-import the regenerated KML into Google My Maps (re-importing, not just refreshing) to confirm the colors actually changed, since My Maps caches styles per import.

## Keep the repository consistent

When a verified fact changes, update every affected source of truth in the same task:

- `.github/instructions/trip-context.instructions.md` for trip-specific baseline facts;
- `Dienu_Planas.txt` for real schedule times and day numbering;
- `Keliones_Asistentas.txt` for logistics, reservations, restaurants, prices, and checklists;
- `tools/gen_day_maps.py` for stops, coordinates, route modes, and map links;
- `<Destination>.kml` only by regenerating it from the generator;
- a calendar reminders file (`.ics`) for check-in windows and boarding/pickup cutoffs, whenever a check-in-bearing
  booking is added or its time changes;
- `README.md` when its summary, links, or reservation list becomes stale.

Review the final diff for stale duplicates and contradictory values. Never update only one occurrence of a fact when other managed files repeat it.

## Keep Codex and Copilot synchronized

Maintain semantic equivalence between the Codex skill and GitHub Copilot agent.

Whenever a user asks to change either agent, or a task changes a durable workflow, verification rule, privacy rule, managed-file convention, or validation rule:

1. Read this shared policy and both agent files.
2. Put platform-neutral behavior in this shared policy whenever possible.
3. Update both agent files in the same task so each points to and enforces the current shared policy.
4. Preserve only necessary platform-specific differences such as YAML frontmatter, tool declarations, UI metadata, and invocation syntax.
5. Compare the final diff of both agent files and confirm that neither contains a contradictory rule.

Do not require automatic commit or push. Commit or push only when the user explicitly asks.
