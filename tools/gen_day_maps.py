#!/usr/bin/env python3
"""Generate one Google My Maps KML file (5 day-layers) for the Iceland trip.

Convention (see .github/agents/trip-planner.agent.md):
- ONE map: 5 days = 5 layers (<Folder>), well under the 10-layer My Maps limit.
- 1 day = 1 layer. Each stop = its own clickable <Placemark> with a Maps link.
- Routes drawn per layer, colour-coded by mode:
    DRIVE -> solid blue   (real road geometry from OSRM)
    WALK  -> green        (straight segment; used for hikes / on-foot stops)
- Each stop's (lon, lat) = the OBJECT / viewpoint you actually visit; the link opens
  its place card (SEARCH[name]) -> tap Directions for live navigation. Route lines are
  only a visual overview (Google Maps does not turn-by-turn along a custom KML line).
  Where parking is far from the object (Thingvellir, Skaftafell), add a separate parking
  pin in the same day layer.

Run:  python3 tools/gen_day_maps.py
Output: Iceland.kml
"""
import json
import re
import urllib.request
from urllib.parse import quote_plus

KEF = (-22.6056, 63.9850)   # KEF (Keflavík) – car pickup / drop-off
VIK = (-19.0061, 63.4186)   # Vík í Mýrdal – restaurants / Katla meeting area
HVO = (-20.2218, 63.7510)   # Hvolsvöllur – fuel / food stop area
PARADISE = (-19.97736, 63.599725)     # Paradise Cave Hostel & Guesthouse
SELFOSS = (-20.9875, 63.9329)         # Gesthús Selfoss – D01 night
SKEIDFLOT = (-19.1899663, 63.4374645) # Skeiðflöt Airbnb – D02–D04 nights

# (lon, lat) -> ASCII place name Google Maps resolves to a place card
# (photo + name + Directions button) instead of bare coordinates.
SEARCH = {
    (-22.6056, 63.9850): "Keflavik Airport",
    (-20.9875, 63.9329): "Gesthus Selfoss Iceland",
    (-21.1300, 64.2558): "Thingvellir National Park",
    (-20.3024, 64.3104): "Strokkur Geysir",
    (-20.3034, 64.3093): "Geysir Center Iceland",
    (-20.3007, 64.3127): "Strokkur Geyser",
    (-20.1199, 64.3271): "Gullfoss",
    (-20.8851, 64.0413): "Kerid Crater",
    (-20.2218, 63.7510): "Hvolsvollur",
    (-19.9774, 63.5997): "Paradise Cave Hostel Guesthouse Seljalandsskola",
    (-19.9886, 63.6156): "Seljalandsfoss",
    (-19.9864, 63.6209): "Gljufrabui",
    (-19.5113, 63.5320): "Skogafoss",
    (-19.5075, 63.5334): "Hestavadfoss",
    (-19.4814, 63.5288): "Kvernufoss",
    (-19.0061, 63.4186): "Vik i Myrdal",
    (-19.1900, 63.4375): "Skeidflot Iceland",
    (-19.0137, 63.4178): "Troll Expeditions Katla Ice Cave Vik",
    (-19.3584, 63.5346): "Solheimajokull",
    (-19.1284, 63.4015): "Dyrholaey",
    (-19.0716, 63.4057): "Reynisfjara Beach",
    (-18.1718, 63.7713): "Fjadrargljufur Canyon",
    (-16.9665, 64.0165): "Skaftafell Visitor Center",
    (-16.1958, 64.0489): "Jokulsarlon Glacier Lagoon",
    (-16.1777, 64.0443): "Diamond Beach Iceland",
    (-21.9265, 64.1420): "Hallgrimskirkja",
    (-21.9224, 64.1475): "Sun Voyager",
    (-21.9463, 64.1165): "Sky Lagoon Iceland",
    (-21.1364, 64.2556): "Thingvellir Parking P1 Hakid",
    (-21.1247, 64.2647): "Almannagjá",
    (-21.1179, 64.2658): "Öxarárfoss",
    (-16.9753, 64.0275): "Svartifoss",
    # parkingai
    (-20.1299, 64.3252): "Gullfoss Upper Car Park",
    (-20.8867, 64.0419): "Kerid Crater Car Park",
    (-19.9938, 63.6157): "Seljalandsfoss Parking",
    (-19.5128, 63.5277): "Skogafoss Car Park",
    (-19.49, 63.5251): "Kvernufoss Parking",
    (-19.3704, 63.5304): "Solheimajokull Parking",
    (-19.1289, 63.4041): "Dyrholaey Parking",
    (-19.0447, 63.4042): "Reynisfjara Car Park",
    (-18.1717, 63.7703): "Fjadrárgljufur Canyon Parking",
    (-16.1797, 64.0480): "Jokulsarlon Glacier Lagoon Parking",
    (-16.1779, 64.0455): "Diamond Beach Parking",
    (-21.9270, 64.1419): "Hallgrimskirkja Parking Lot",
}

# Direct CID links overriding SEARCH (verified Google Maps place cards)
LINKS = {
    (-20.1299, 64.3252): "https://maps.google.com/?cid=10988653360962908817",  # Gullfoss parkingas
    (-16.1797, 64.0480): "https://maps.google.com/?cid=18024857851449796574",  # Jökulsárlón Glacier Lagoon Parking
    (-16.1779, 64.0455): "https://maps.google.com/?cid=4059657798852550162",   # Diamond Beach Parking
    (-21.9270, 64.1419): "https://maps.google.com/?cid=8301664305105330080",    # Hallgrímskirkja parkingas
}

# kind -> icon colour (KML aabbggrr)
KINDS = {
    "hotel": ("ff37a000", "grn-circle"),     # green
    "parking": ("ffdb1e1e", "blu-circle"),   # blue
    "sight": ("ff0000ff", "red-circle"),     # red
    "food": ("ff00a5ff", "orange-circle"),   # orange
    "beach": ("ff00d7ff", "ylw-circle"),     # yellow
    "transit": ("ff800080", "purple-circle"),
}

# Each stop: (name, lon, lat, kind, mode_to_reach)  mode in start|drive|walk
DAYS = {
    1: ("01 – Atvykimas → Selfoss", [
        ("Keflavik oro uostas", KEF[0], KEF[1], "transit", "start"),
        ("Nakvynė – Gesthús Selfoss", SELFOSS[0], SELFOSS[1], "hotel", "drive"),
    ]),
    2: ("02 – Auksinis ratas + Kriokliai ⚠️ ILGA DIENA", [
        ("Nakvynė – Gesthús Selfoss", SELFOSS[0], SELFOSS[1], "hotel", "start"),
        # Þingvellir: važiuojame iki P1 aikštelės, pėsčiomis per parką, grįžtame į P1
        ("🅿️ Þingvellir P1 – Hakið", -21.13639, 64.25564, "parking", "drive"),
        ("Almannagjá plyšys + Lögberg", -21.1247222, 64.2647222, "sight", "walk"),
        ("Öxarárfoss krioklys", -21.117885, 64.2658062, "sight", "walk"),
        ("🅿️ P1 – grįžimas prie automobilio", -21.13639, 64.25564, "parking", "walk", False),
        ("🅿️ Geysir parkingas", -20.30337, 64.30927, "parking", "drive"),
        ("Strokkur geizeris", -20.3007211, 64.3127094, "sight", "walk"),
        ("🅿️ Geysir (grįžimas prie automobilio)", -20.30337, 64.30927, "parking", "walk", False),
        ("🅿️ Gullfoss parkingas", -20.1299, 64.3252, "parking", "drive"),
        ("Gullfoss krioklys", -20.1199, 64.3271, "sight", "walk"),
        ("🅿️ Gullfoss (grįžimas prie automobilio)", -20.1299, 64.3252, "parking", "walk", False),
        ("🅿️ Kerið parkingas", -20.8867, 64.0419, "parking", "drive"),
        ("Kerið krateris", -20.8851, 64.0413, "sight", "walk"),
        ("🅿️ Kerið (grįžimas prie automobilio)", -20.8867, 64.0419, "parking", "walk", False),
        ("🅿️ Seljalandsfoss parkingas", -19.9938, 63.6157, "parking", "drive"),
        ("Seljalandsfoss krioklys", -19.9886, 63.6156, "sight", "walk"),
        ("Gljúfrabúi krioklys", -19.9864, 63.6209, "sight", "walk"),
        ("🅿️ Seljalandsfoss (grįžimas prie automobilio)", -19.9938, 63.6157, "parking", "walk", False),
        ("🅿️ Kvernufoss parkingas", -19.49, 63.5251, "parking", "drive"),
        ("Kvernufoss krioklys", -19.4814, 63.5288, "sight", "walk"),
        ("🅿️ Kvernufoss (grįžimas prie automobilio)", -19.49, 63.5251, "parking", "walk", False),
        ("Nakvynė – Skeiðflöt", SKEIDFLOT[0], SKEIDFLOT[1], "hotel", "drive"),
    ]),
    3: ("03 – Waterfall Way + Katla + Krantas", [
        ("Nakvynė – Skeiðflöt", SKEIDFLOT[0], SKEIDFLOT[1], "hotel", "start"),
        ("🅿️ Skógafoss parkingas", -19.5128, 63.5277, "parking", "drive"),
        ("Skógafoss krioklys", -19.5113, 63.5320, "sight", "walk"),
        ("Hestavaðsfoss", -19.5075, 63.5334, "sight", "walk"),
        ("🅿️ Skógafoss (grįžimas prie automobilio)", -19.5128, 63.5277, "parking", "walk", False),
        ("🅿️ Sólheimajökull parkingas", -19.3704, 63.5304, "parking", "drive"),
        ("Sólheimajökull ledynas", -19.3584, 63.5346, "sight", "walk"),
        ("🅿️ Sólheimajökull (grįžimas prie automobilio)", -19.3704, 63.5304, "parking", "walk", False),
        ("Katla ledo urvas – Tröll Expeditions", -19.0137, 63.4178, "sight", "drive"),
        ("🅿️ Reynisfjara parkingas", -19.0447, 63.4042, "parking", "drive"),
        ("Reynisfjara juodas paplūdimys", -19.0716, 63.4057, "beach", "walk"),
        ("🅿️ Reynisfjara (grįžimas prie automobilio)", -19.0447, 63.4042, "parking", "walk", False),
        ("🅿️ Dyrhólaey parkingas", -19.1289, 63.4041, "parking", "drive"),
        ("Dyrhólaey", -19.1284, 63.4015, "sight", "walk"),
        ("🅿️ Dyrhólaey (grįžimas prie automobilio)", -19.1289, 63.4041, "parking", "walk", False),
        ("Nakvynė – Skeiðflöt", SKEIDFLOT[0], SKEIDFLOT[1], "hotel", "drive"),
    ]),
    4: ("04 – Jökulsárlón + Skaftafell ⚠️ ILGA DIENA", [
        ("Nakvynė – Skeiðflöt", SKEIDFLOT[0], SKEIDFLOT[1], "hotel", "start"),
        ("🅿️ Fjaðrárgljúfur parkingas", -18.1717, 63.7703, "parking", "drive"),
        ("Fjaðrárgljúfur kanjonas", -18.1718, 63.7713, "sight", "walk"),
        ("🅿️ Fjaðrárgljúfur (grįžimas prie automobilio)", -18.1717, 63.7703, "parking", "walk", False),
        # Skaftafell: važiuojame iki lankytojų centro, ~1.5 km pėsčiomis iki Svartifoss
        ("🅿️ Skaftafell lankytojų centras", -16.9665, 64.0165, "parking", "drive"),
        ("Svartifoss krioklys", -16.9753, 64.0275, "sight", "walk"),
        ("🅿️ Skaftafell (grįžimas prie automobilio)", -16.9665, 64.0165, "parking", "walk", False),
        ("🅿️ Diamond Beach parkingas", -16.1779, 64.0455, "parking", "drive"),
        ("Diamond Beach", -16.1777, 64.0443, "beach", "walk"),
        ("🅿️ Diamond Beach (grįžimas prie automobilio)", -16.1779, 64.0455, "parking", "walk", False),
        ("🅿️ Jökulsárlón parkingas", -16.17974, 64.04804, "parking", "drive"),
        ("Jökulsárlón ledynų lagūna", -16.1958, 64.0489, "sight", "walk"),
        ("🅿️ Jökulsárlón (grįžimas prie automobilio)", -16.17974, 64.04804, "parking", "walk", False),
        ("Nakvynė – Skeiðflöt", SKEIDFLOT[0], SKEIDFLOT[1], "hotel", "drive"),
    ]),
    5: ("05 – Reykjavík + Sky Lagoon + išvykimas", [
        ("Nakvynė – Skeiðflöt", SKEIDFLOT[0], SKEIDFLOT[1], "hotel", "start"),
        ("🅿️ Hallgrímskirkja parkingas", -21.92697, 64.1419, "parking", "drive"),
        ("Hallgrímskirkja", -21.92654, 64.14202, "sight", "walk"),
        ("Sun Voyager / Harpa", -21.9224, 64.1475, "sight", "walk"),
        ("🅿️ Reykjavík (grīžimas prie automobilio)", -21.92697, 64.1419, "parking", "walk", False),
        ("Sky Lagoon (Kópavogur)", -21.94629, 64.11648, "sight", "drive"),
        ("Keflavik oro uostas", KEF[0], KEF[1], "transit", "drive"),
    ]),
}

LINE_STYLES = {
    "drive": ("ffff0000", 5),    # blue
    "walk": ("ff008000", 4),     # green
}


def osrm_geometry(a, b):
    """Return list of (lon,lat) following roads, or [a,b] on failure."""
    url = (f"http://router.project-osrm.org/route/v1/driving/"
           f"{a[0]},{a[1]};{b[0]},{b[1]}?overview=full&geometries=geojson")
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            d = json.load(r)
        return [(c[0], c[1]) for c in d["routes"][0]["geometry"]["coordinates"]]
    except Exception:
        return [a, b]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def maps_link(name, lon, lat):
    key = (round(lon, 4), round(lat, 4))
    direct = LINKS.get(key)
    if direct:
        return direct
    term = SEARCH.get(key)
    if not term:
        # fall back to the placemark name with emoji/index stripped
        term = re.sub(r"[^\w\s/().\-]", "", name, flags=re.UNICODE).strip()
    return f"https://www.google.com/maps/search/?api=1&query={quote_plus(term)}"


def build_day_folder(day, title, stops):
    out = [f"    <Folder>\n      <name>DIENA {esc(title)}</name>"]
    # route lines first (so pins render on top)
    for i in range(1, len(stops)):
        prev = stops[i - 1]
        cur = stops[i]
        mode = cur[4]
        a = (prev[1], prev[2])
        b = (cur[1], cur[2])
        if mode == "drive":
            pts = osrm_geometry(a, b)
            if pts:          # anchor endpoints to exact stop coords (avoids OSRM snap offset)
                pts[0] = a
                pts[-1] = b
        else:
            pts = [a, b]
        color, width = LINE_STYLES.get(mode, LINE_STYLES["walk"])
        coordstr = " ".join(f"{x},{y},0" for x, y in pts)
        label = {"drive": "🚗 Vairavimas", "walk": "🚶 Ėjimas / hike"}.get(mode, mode)
        out.append(
            "      <Placemark>\n"
            f"        <name>{label}: {esc(prev[0])} → {esc(cur[0])}</name>\n"
            "        <Style><LineStyle>"
            f"<color>{color}</color><width>{width}</width>"
            "</LineStyle></Style>\n"
            "        <LineString><tessellate>1</tessellate>"
            f"<coordinates>{coordstr}</coordinates></LineString>\n"
            "      </Placemark>"
        )
    # stop pins
    for idx, stop in enumerate(stops, 1):
        name, lon, lat, kind, mode = stop[:5]
        show_pin = stop[5] if len(stop) > 5 else True
        if not show_pin:
            continue
        color, _ = KINDS.get(kind, KINDS["sight"])
        link = maps_link(name, lon, lat)
        desc = f"<![CDATA[🔗 <a href=\"{link}\">{link}</a>]]>"
        out.append(
            "      <Placemark>\n"
            f"        <name>{esc(name)}</name>\n"
            f"        <description>{desc}</description>\n"
            "        <Style><IconStyle>"
            f"<color>{color}</color><scale>1.1</scale>"
            "<Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon>"
            "</IconStyle></Style>\n"
            f"        <Point><coordinates>{lon},{lat},0</coordinates></Point>\n"
            "      </Placemark>"
        )
    out.append("    </Folder>")
    return "\n".join(out)


def build_map(name, day_range):
    folders = []
    for day in day_range:
        title, stops = DAYS[day]
        print(f"  building DIENA {title} ...")
        folders.append(build_day_folder(day, title, stops))
    body = "\n".join(folders)
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n"
        "  <Document>\n"
        f"    <name>{esc(name)}</name>\n"
        "    <description><![CDATA[🚗 mėlyna = vairavimas (keliai) · "
        "🚶 žalia = ėjimas / hike. "
        "1 diena = 1 sluoksnis. Kiekvienas taškas – paspaudžiamas su nuoroda.]]></description>\n"
        f"{body}\n"
        "  </Document>\n"
        "</kml>\n"
    )


def main():
    print("Iceland day map (D01-05):")
    m = build_map("Islandija – Dienų maršrutai 01–05", range(1, 6))
    with open("Iceland.kml", "w", encoding="utf-8") as f:
        f.write(m)
    print("Done -> Iceland.kml")


if __name__ == "__main__":
    main()
