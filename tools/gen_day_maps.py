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
Output: Iceland_Dienos.kml
"""
import json
import re
import urllib.request
from urllib.parse import quote_plus

KEF = (-22.6056, 63.9850)   # KEF (Keflavík) – car pickup / drop-off
VIK = (-19.0061, 63.4186)   # Vík í Mýrdal – base for D02–D04 nights
HVO = (-20.2218, 63.7510)   # Hvolsvöllur – D01 night

# (lon, lat) -> ASCII place name Google Maps resolves to a place card
# (photo + name + Directions button) instead of bare coordinates.
SEARCH = {
    (-22.6056, 63.9850): "Keflavik Airport",
    (-21.1300, 64.2558): "Thingvellir National Park",
    (-20.3024, 64.3104): "Strokkur Geysir",
    (-20.1206, 64.3271): "Gullfoss",
    (-20.8856, 64.0414): "Kerid Crater",
    (-20.2218, 63.7510): "Hvolsvollur",
    (-19.9926, 63.6156): "Seljalandsfoss",
    (-19.9886, 63.6190): "Gljufrabui",
    (-19.5111, 63.5320): "Skogafoss",
    (-19.5089, 63.5360): "Skogafoss",
    (-19.4906, 63.5316): "Kvernufoss",
    (-19.0061, 63.4186): "Vik i Myrdal",
    (-19.3692, 63.5300): "Solheimajokull",
    (-19.1276, 63.4017): "Dyrholaey",
    (-19.0448, 63.4054): "Reynisfjara Beach",
    (-18.1718, 63.7714): "Fjadrargljufur Canyon",
    (-16.9665, 64.0159): "Svartifoss",
    (-16.1794, 64.0484): "Jokulsarlon Glacier Lagoon",
    (-16.1755, 64.0432): "Diamond Beach Iceland",
    (-21.9266, 64.1417): "Hallgrimskirkja",
    (-21.9224, 64.1475): "Sun Voyager",
    (-21.9436, 64.1188): "Sky Lagoon Iceland",
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
    1: ("01 – Atvykimas + Auksinis ratas", [
        ("Keflavik oro uostas", KEF[0], KEF[1], "parking", "start"),
        ("Þingvellir nacionalinis parkas", -21.1300, 64.2558, "sight", "drive"),
        ("Geysir / Strokkur", -20.3024, 64.3104, "sight", "drive"),
        ("Gullfoss krioklys", -20.1206, 64.3271, "sight", "drive"),
        ("Kerið krateris", -20.8856, 64.0414, "sight", "drive"),
        ("Nakvynė – Hvolsvöllur", HVO[0], HVO[1], "hotel", "drive"),
    ]),
    2: ("02 – Kriokliai + Waterfall Way hike", [
        ("Nakvynė – Hvolsvöllur", HVO[0], HVO[1], "hotel", "start"),
        ("Seljalandsfoss krioklys", -19.9926, 63.6156, "sight", "drive"),
        ("Gljúfrabúi krioklys", -19.9886, 63.6190, "sight", "walk"),
        ("Skógafoss krioklys", -19.5111, 63.5320, "sight", "drive"),
        ("🥾 Waterfall Way (Skógá takas)", -19.5089, 63.5360, "sight", "walk"),
        ("Kvernufoss krioklys", -19.4906, 63.5316, "sight", "drive"),
        ("Nakvynė – Vík", VIK[0], VIK[1], "hotel", "drive"),
    ]),
    3: ("03 – Sólheimajökull + Reynisfjara + Katla ledo urvas", [
        ("Nakvynė – Vík", VIK[0], VIK[1], "hotel", "start"),
        ("Sólheimajökull ledynas", -19.3692, 63.5300, "sight", "drive"),
        ("Dyrhólaey", -19.1276, 63.4017, "sight", "drive"),
        ("Reynisfjara juodas paplūdimys", -19.0448, 63.4054, "beach", "drive"),
        ("🕳️ Katla ledo urvas (tūras iš Vík)", VIK[0], VIK[1], "sight", "drive"),
    ]),
    4: ("04 – Jökulsárlón + Skaftafell ⚠️", [
        ("Nakvynė – Vík", VIK[0], VIK[1], "hotel", "start"),
        ("Fjaðrárgljúfur kanjonas", -18.1718, 63.7714, "sight", "drive"),
        ("Skaftafell – Svartifoss", -16.9665, 64.0159, "sight", "drive"),
        ("Jökulsárlón ledynų lagūna", -16.1794, 64.0484, "sight", "drive"),
        ("Diamond Beach", -16.1755, 64.0432, "beach", "walk"),
        ("Nakvynė – Vík", VIK[0], VIK[1], "hotel", "drive"),
    ]),
    5: ("05 – Reykjavík + Sky Lagoon + išvykimas", [
        ("Nakvynė – Vík", VIK[0], VIK[1], "hotel", "start"),
        ("Reykjavík – Hallgrímskirkja", -21.9266, 64.1417, "sight", "drive"),
        ("Sun Voyager / Harpa", -21.9224, 64.1475, "sight", "walk"),
        ("Sky Lagoon (Kópavogur)", -21.9436, 64.1188, "sight", "drive"),
        ("KEF – auto grąžinimas + skrydis", KEF[0], KEF[1], "parking", "drive"),
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
    term = SEARCH.get((round(lon, 4), round(lat, 4)))
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
    for idx, (name, lon, lat, kind, mode) in enumerate(stops, 1):
        color, _ = KINDS.get(kind, KINDS["sight"])
        link = maps_link(name, lon, lat)
        desc = (f"<![CDATA[{idx}. {esc(name)}<br>🔗 "
                f"<a href=\"{link}\">{link}</a>]]>")
        out.append(
            "      <Placemark>\n"
            f"        <name>{idx}. {esc(name)}</name>\n"
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
    with open("Iceland_Dienos.kml", "w", encoding="utf-8") as f:
        f.write(m)
    print("Done -> Iceland_Dienos.kml")


if __name__ == "__main__":
    main()
