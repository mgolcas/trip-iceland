# Islandija 2026 🇮🇸

Pietinės pakrantės kelionė nuomotu automobiliu: **2026.09.07 – 2026.09.11** (5 dienos, 3 keliautojai).
Skrydis Vilnius → KEF (Keflavík), maršrutas Ring Road (Kelias 1) palei pietinę pakrantę,
daug gamtos, kriokliai ir 2–3 val. žygis (Waterfall Way).

Automobilis: **Zero Car – Dacia Duster 4WD, mechaninis; rezervacija perkelta į 09.07 17:00–09.11 17:00**.

## Failai

| Failas | Paskirtis |
|--------|-----------|
| [`Dienu_Planas.txt`](Dienu_Planas.txt) | Pagrindinis dienų planas su tikslais laikais (MASTER) |
| [`Keliones_Asistentas.txt`](Keliones_Asistentas.txt) | Pasiruošimo sąrašas: skrydžiai, auto nuoma, degalai, orai, sauga |
| [`Islandija_Priminimai.ics`](Islandija_Priminimai.ics) | Check-in/boarding priminimai kalendoriui (Zero Car, skrydžiai) |
| [`Iceland.kml`](Iceland.kml) | Dienų žemėlapis (5 sluoksniai D01–D05) – auto-generuojamas |
| [`tools/gen_day_maps.py`](tools/gen_day_maps.py) | Dienų žemėlapio generatorius (OSRM kelių geometrija) |

## Žemėlapių importas

Importuok `Iceland.kml` į [Google My Maps](https://www.google.com/mymaps).

## Priminimų importas į kalendorių

`Islandija_Priminimai.ics` turi 6 priminimus (Zero Car online check-in atsidarymas ir paskutinė
proga, skrydžių online check-in atsidarymas, ėjimas į išvykimo vartus – abiem skrydžiams).

- **Google Calendar** (kompiuteryje): Settings → Import & export → Import → pasirink
  `Islandija_Priminimai.ics` → Import. Telefone „+" mygtukas neimportuoja failų – naudok
  kompiuterio naršyklę arba atidaryk failą telefone ir pasirink „Open with Google Calendar".
- **Apple Calendar** (iPhone/iPad/Mac): atidaryk `.ics` failą (pvz., iš pašto priedo ar Files
  app) – jis automatiškai pasiūlys pridėti įvykius į pasirinktą kalendorių.
- Visi laikai faile yra UTC (`Z` žymė), todėl kiekvienas įrenginys automatiškai parodys
  teisingą vietos laiką nepriklausomai nuo laiko juostos.


## Maršruto santrauka

- **D01 09.07** – Vakarinis atvykimas → Gesthús Selfoss
- **D02 09.08** – Auksinis ratas + Seljalandsfoss, Gljúfrabúi, Kvernufoss → Skeiðflöt
- **D03 09.09** – Waterfall Way + Sólheimajökull + Katla + Reynisfjara, Dyrhólaey
- **D04 09.10** – Jökulsárlón Zodiac 15:10 ✅ + Skaftafell + Fjaðrárgljúfur ⚠️ ilga diena
- **D05 09.11** – Trumpas Reykjavík + Sky Lagoon + išvykimas

Planavimo agentas ir konvencijos: [`.github/agents/trip-planner.agent.md`](.github/agents/trip-planner.agent.md)
(GitHub Copilot) arba [`.agents/skills/trip-planner/SKILL.md`](.agents/skills/trip-planner/SKILL.md) (Codex) –
abu remiasi ta pačia bendra politika [`.github/instructions/trip-planner-shared.instructions.md`](.github/instructions/trip-planner-shared.instructions.md)
ir šios kelionės duomenimis [`.github/instructions/trip-context.instructions.md`](.github/instructions/trip-context.instructions.md).
