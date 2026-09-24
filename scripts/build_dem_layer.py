#!/usr/bin/env python3
"""
Build public/nj07-voters.geojson — no external dependencies required.

Downloads NJ municipality boundaries from NJGIN, clips to NJ-07 via
centroid-in-polygon test, joins placeholder voter registration data,
and writes the output GeoJSON.

Usage:
    python3 scripts/build_dem_layer.py

Updating voter registration data:
    1. Go to https://www.nj.gov/state/elections/election-information-svrs.shtml
    2. Download the most recent SVRS report (PDF).
    3. Find the per-municipality counts for each county that overlaps NJ-07.
    4. Update VOTER_REG below with (dem_registered, unaffiliated_registered, total_registered) triples.
    5. Re-run this script to regenerate public/nj07-voters.geojson.
"""

import json, sys, urllib.request, urllib.parse
from pathlib import Path

DISTRICT_PATH = Path("public/nj07.geojson")
OUTPUT_PATH   = Path("public/nj07-voters.geojson")

# NJGIN Open Data – Municipal Boundaries of NJ (GeoJSON, WGS84)
# Dataset: https://njogis-newjersey.opendata.arcgis.com/datasets/municipal-boundaries-of-nj/
MUNIS_URL = (
    "https://opendata.arcgis.com/api/v3/datasets/"
    "1c6b26a9a14e4132895194e80d6b30f8/downloads/data"
    "?format=geojson&spatialRefId=4326"
)

# ---------------------------------------------------------------------------
# Voter registration data  (PLACEHOLDER – replace with NJ SVRS report values)
# Key:   (county_name_upper, municipality_label_upper)
# Value: (dem_registered, total_registered)
#
# County FIPS in NJ-07: Essex(013) Hunterdon(019) Morris(027)
#                       Somerset(035) Union(039) Warren(041)
#
# Run the script once with an empty dict to see what keys are printed for
# unmatched municipalities, then fill them in here.
# ---------------------------------------------------------------------------
VOTER_REG: dict[tuple[str, str], tuple[int, int, int]] = {
    # -----------------------------------------------------------------------
    # PLACEHOLDER values — replace with real data from the NJ SVRS report.
    # Keys match the NJGIN MUN_LABEL / COUNTY property values exactly.
    # Values: (dem_registered, unaffiliated_registered, total_registered)
    # -----------------------------------------------------------------------

    # Hunterdon County (~40% Dem, ~30% unaffiliated)
    ("HUNTERDON", "ALEXANDRIA TOWNSHIP"):      ( 1050,  900,  3000),
    ("HUNTERDON", "BETHLEHEM TOWNSHIP"):       (  825,  750,  2500),
    ("HUNTERDON", "BLOOMSBURY BOROUGH"):       (  320,  240,   800),
    ("HUNTERDON", "CALIFON BOROUGH"):          (  294,  210,   700),
    ("HUNTERDON", "CLINTON TOWN"):             ( 1350,  900,  3000),
    ("HUNTERDON", "CLINTON TOWNSHIP"):         ( 3800, 2850,  9500),
    ("HUNTERDON", "DELAWARE TOWNSHIP"):        ( 1330, 1050,  3500),
    ("HUNTERDON", "EAST AMWELL TOWNSHIP"):     ( 1200,  900,  3000),
    ("HUNTERDON", "FLEMINGTON BOROUGH"):       ( 1664,  960,  3200),
    ("HUNTERDON", "FRANKLIN TOWNSHIP"):        ( 1330, 1050,  3500),
    ("HUNTERDON", "FRENCHTOWN BOROUGH"):       (  660,  360,  1200),
    ("HUNTERDON", "GLEN GARDNER BOROUGH"):     (  266,  210,   700),
    ("HUNTERDON", "HAMPTON BOROUGH"):          (  360,  270,   900),
    ("HUNTERDON", "HIGH BRIDGE BOROUGH"):      ( 1260,  840,  2800),
    ("HUNTERDON", "HOLLAND TOWNSHIP"):         ( 1120,  960,  3200),
    ("HUNTERDON", "KINGWOOD TOWNSHIP"):        (  925,  750,  2500),
    ("HUNTERDON", "LAMBERTVILLE CITY"):        ( 1625,  750,  2500),
    ("HUNTERDON", "LEBANON BOROUGH"):          (  600,  450,  1500),
    ("HUNTERDON", "LEBANON TOWNSHIP"):         ( 1665, 1350,  4500),
    ("HUNTERDON", "MILFORD BOROUGH"):          (  384,  240,   800),
    ("HUNTERDON", "RARITAN TOWNSHIP"):         ( 7200, 5400, 18000),
    ("HUNTERDON", "READINGTON TOWNSHIP"):      ( 4620, 3300, 11000),
    ("HUNTERDON", "STOCKTON BOROUGH"):         (  220,  120,   400),
    ("HUNTERDON", "TEWKSBURY TOWNSHIP"):       ( 2204, 1740,  5800),
    ("HUNTERDON", "UNION TOWNSHIP"):           ( 1110,  900,  3000),
    ("HUNTERDON", "WEST AMWELL TOWNSHIP"):     ( 1200,  900,  3000),

    # Morris County (~44% Dem, ~27% unaffiliated)
    ("MORRIS", "CHESTER BOROUGH"):             (  924,  594,  2200),
    ("MORRIS", "CHESTER TOWNSHIP"):            ( 2800, 1890,  7000),
    ("MORRIS", "LONG HILL TOWNSHIP"):          ( 2700, 1620,  6000),
    ("MORRIS", "MENDHAM BOROUGH"):             ( 1596, 1134,  4200),
    ("MORRIS", "MENDHAM TOWNSHIP"):            ( 2072, 1512,  5600),
    ("MORRIS", "MINE HILL TOWNSHIP"):          ( 1125,  675,  2500),
    ("MORRIS", "MOUNT ARLINGTON BOROUGH"):     ( 1440,  810,  3000),
    ("MORRIS", "MOUNT OLIVE TOWNSHIP"):        ( 5750, 3375, 12500),
    ("MORRIS", "NETCONG BOROUGH"):             (  765,  459,  1700),
    ("MORRIS", "ROXBURY TOWNSHIP"):            ( 5940, 3645, 13500),
    ("MORRIS", "WASHINGTON TOWNSHIP"):         ( 5060, 3105, 11500),
    ("MORRIS", "WHARTON BOROUGH"):             ( 1598,  918,  3400),

    # Somerset County (~47% Dem, ~28% unaffiliated)
    ("SOMERSET", "BEDMINSTER TOWNSHIP"):       ( 1596, 1176,  4200),
    ("SOMERSET", "BERNARDS TOWNSHIP"):         ( 7200, 4480, 16000),
    ("SOMERSET", "BERNARDSVILLE BOROUGH"):     ( 2420, 1540,  5500),
    ("SOMERSET", "BRANCHBURG TOWNSHIP"):       ( 4230, 2520,  9000),
    ("SOMERSET", "BRIDGEWATER TOWNSHIP"):      (13800, 8400, 30000),
    ("SOMERSET", "FAR HILLS BOROUGH"):         (  385,  308,  1100),
    ("SOMERSET", "GREEN BROOK TOWNSHIP"):      ( 2250, 1260,  4500),
    ("SOMERSET", "PEAPACK-GLADSTONE BOROUGH"): (  880,  616,  2200),
    ("SOMERSET", "RARITAN BOROUGH"):           ( 2300, 1288,  4600),
    ("SOMERSET", "SOMERVILLE BOROUGH"):        ( 3080, 1540,  5500),
    ("SOMERSET", "WARREN TOWNSHIP"):           ( 4320, 2520,  9000),
    ("SOMERSET", "WATCHUNG BOROUGH"):          ( 1600,  896,  3200),

    # Sussex County (~38% Dem, ~32% unaffiliated)
    ("SUSSEX", "ANDOVER BOROUGH"):             (  228,  192,   600),
    ("SUSSEX", "BYRAM TOWNSHIP"):              ( 2600, 2080,  6500),
    ("SUSSEX", "FREDON TOWNSHIP"):             (  630,  576,  1800),
    ("SUSSEX", "GREEN TOWNSHIP"):              (  700,  640,  2000),
    ("SUSSEX", "HOPATCONG BOROUGH"):           ( 3360, 2560,  8000),
    ("SUSSEX", "OGDENSBURG BOROUGH"):          (  720,  576,  1800),
    ("SUSSEX", "SPARTA TOWNSHIP"):             ( 5320, 4480, 14000),
    ("SUSSEX", "STANHOPE BOROUGH"):            (  860,  640,  2000),
    ("SUSSEX", "STILLWATER TOWNSHIP"):         (  875,  800,  2500),
    ("SUSSEX", "WALPACK TOWNSHIP"):            (   40,   32,   100),

    # Union County (~57% Dem, ~22% unaffiliated)
    ("UNION", "BERKELEY HEIGHTS TOWNSHIP"):    ( 4784, 2024,  9200),
    ("UNION", "CLARK TOWNSHIP"):               ( 4680, 1980,  9000),
    ("UNION", "FANWOOD BOROUGH"):              ( 2580,  946,  4300),
    ("UNION", "LINDEN CITY"):                  (12240, 3960, 18000),
    ("UNION", "MOUNTAINSIDE BOROUGH"):         ( 1170,  572,  2600),
    ("UNION", "NEW PROVIDENCE BOROUGH"):       ( 3672, 1496,  6800),
    ("UNION", "RAHWAY CITY"):                  ( 8450, 2860, 13000),
    ("UNION", "SCOTCH PLAINS TOWNSHIP"):       ( 7125, 2750, 12500),
    ("UNION", "SPRINGFIELD TOWNSHIP"):         ( 4860, 1980,  9000),
    ("UNION", "SUMMIT CITY"):                  ( 8550, 3300, 15000),
    ("UNION", "WESTFIELD TOWN"):               ( 7695, 2970, 13500),
    ("UNION", "WINFIELD TOWNSHIP"):            (  220,   88,   400),

    # Warren County (~38% Dem, ~30% unaffiliated)
    ("WARREN", "ALLAMUCHY TOWNSHIP"):          ( 1225, 1050,  3500),
    ("WARREN", "ALPHA BOROUGH"):               (  720,  540,  1800),
    ("WARREN", "BELVIDERE TOWN"):              (  756,  540,  1800),
    ("WARREN", "BLAIRSTOWN TOWNSHIP"):         ( 1295, 1050,  3500),
    ("WARREN", "FRANKLIN TOWNSHIP"):           (  980,  840,  2800),
    ("WARREN", "FRELINGHUYSEN TOWNSHIP"):      (  396,  360,  1200),
    ("WARREN", "GREENWICH TOWNSHIP"):          ( 1216,  960,  3200),
    ("WARREN", "HACKETTSTOWN TOWN"):           ( 2000, 1500,  5000),
    ("WARREN", "HARDWICK TOWNSHIP"):           (  396,  360,  1200),
    ("WARREN", "HARMONY TOWNSHIP"):            (  770,  660,  2200),
    ("WARREN", "HOPE TOWNSHIP"):               (  525,  450,  1500),
    ("WARREN", "INDEPENDENCE TOWNSHIP"):       ( 1295, 1050,  3500),
    ("WARREN", "LIBERTY TOWNSHIP"):            (  770,  660,  2200),
    ("WARREN", "LOPATCONG TOWNSHIP"):          ( 2100, 1500,  5000),
    ("WARREN", "MANSFIELD TOWNSHIP"):          ( 1900, 1500,  5000),
    ("WARREN", "OXFORD TOWNSHIP"):             (  950,  750,  2500),
    ("WARREN", "PHILLIPSBURG TOWN"):           ( 2340, 1560,  5200),
    ("WARREN", "POHATCONG TOWNSHIP"):          (  950,  750,  2500),
    ("WARREN", "WASHINGTON BOROUGH"):          ( 1470, 1050,  3500),
    ("WARREN", "WASHINGTON TOWNSHIP"):         ( 2775, 2250,  7500),
    ("WARREN", "WHITE TOWNSHIP"):              ( 1050,  900,  3000),
}


# ---------------------------------------------------------------------------
# Pure-Python spatial helpers
# ---------------------------------------------------------------------------

def _ring_contains(ring: list, px: float, py: float) -> bool:
    """Ray-casting point-in-polygon for one exterior/hole ring."""
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > py) != (yj > py):
            if px < (xj - xi) * (py - yi) / (yj - yi) + xi:
                inside = not inside
        j = i
    return inside


def geometry_contains(geom: dict, px: float, py: float) -> bool:
    """Test if a GeoJSON Polygon or MultiPolygon contains (px, py)."""
    t = geom["type"]
    if t == "Polygon":
        rings = geom["coordinates"]
        if not _ring_contains(rings[0], px, py):
            return False
        return not any(_ring_contains(h, px, py) for h in rings[1:])
    if t == "MultiPolygon":
        return any(
            geometry_contains({"type": "Polygon", "coordinates": poly}, px, py)
            for poly in geom["coordinates"]
        )
    return False


def ring_centroid(ring: list) -> tuple[float, float]:
    xs = [c[0] for c in ring]
    ys = [c[1] for c in ring]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def geometry_centroid(geom: dict) -> tuple[float, float] | None:
    t = geom["type"]
    if t == "Polygon":
        return ring_centroid(geom["coordinates"][0])
    if t == "MultiPolygon":
        largest = max(geom["coordinates"], key=lambda p: len(p[0]))
        return ring_centroid(largest[0])
    return None


# ---------------------------------------------------------------------------

def load_district(path: Path) -> list[dict]:
    raw = json.loads(path.read_text())
    if raw.get("type") == "FeatureCollection":
        return [f["geometry"] for f in raw["features"]]
    if raw.get("type") == "Feature":
        return [raw["geometry"]]
    return [raw]


def detect_name_fields(props: dict) -> tuple[str | None, str | None]:
    """Guess which property keys hold the municipality name and county name."""
    name_candidates   = ["MUN_LABEL", "NAME", "MUNI_NAME", "MUNICIPALITY"]
    county_candidates = ["COUNTY", "CO_NAME", "COUNTY_NAME"]
    name_key   = next((k for k in name_candidates   if k in props), None)
    county_key = next((k for k in county_candidates if k in props), None)
    return name_key, county_key


def main() -> None:
    if not DISTRICT_PATH.exists():
        sys.exit(f"District file not found: {DISTRICT_PATH}")

    district_geoms = load_district(DISTRICT_PATH)

    def in_district(px: float, py: float) -> bool:
        return any(geometry_contains(g, px, py) for g in district_geoms)

    print(f"Downloading NJ municipality boundaries from NJGIN…")
    try:
        req = urllib.request.Request(MUNIS_URL, headers={"User-Agent": "build_dem_layer/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            munis_fc = json.loads(r.read())
    except Exception as e:
        sys.exit(
            f"Download failed: {e}\n\n"
            "Manually download the GeoJSON from:\n"
            "  https://njogis-newjersey.opendata.arcgis.com/datasets/municipal-boundaries-of-nj/\n"
            "Save it as /tmp/nj_munis.geojson, then re-run with MUNIS_URL pointing to that file."
        )

    features = munis_fc.get("features", [])
    print(f"Total NJ municipalities downloaded: {len(features)}")

    if not features:
        sys.exit("No features in downloaded GeoJSON.")

    # Auto-detect property field names from first feature
    first_props = features[0]["properties"]
    name_key, county_key = detect_name_fields(first_props)
    if name_key is None or county_key is None:
        print("Available properties:", list(first_props.keys()))
        sys.exit(
            "Could not auto-detect name/county fields. "
            "Update detect_name_fields() with the correct keys from the list above."
        )
    print(f"Using fields: name='{name_key}', county='{county_key}'")

    output_features = []
    unmatched: list[str] = []

    for feat in features:
        geom = feat.get("geometry")
        if geom is None:
            continue
        centroid = geometry_centroid(geom)
        if centroid is None:
            continue
        cx, cy = centroid
        if not in_district(cx, cy):
            continue

        props   = feat["properties"]
        raw_name   = str(props.get(name_key, "")).strip().upper()
        raw_county = str(props.get(county_key, "")).strip().upper()

        pair = VOTER_REG.get((raw_county, raw_name))
        if pair is None:
            unmatched.append(f'("{raw_county}", "{raw_name}")')
            pct_dem = pct_unaff = pct_rep = None
        else:
            dem, unaff, total = pair
            pct_dem   = round(dem   / total * 100, 1) if total > 0 else None
            pct_unaff = round(unaff / total * 100, 1) if total > 0 else None
            pct_rep   = round((total - dem - unaff) / total * 100, 1) if total > 0 else None

        output_features.append({
            "type": "Feature",
            "geometry": geom,
            "properties": {
                "municipality":    props.get(name_key, ""),
                "county":          props.get(county_key, ""),
                "pct_dem":         pct_dem,
                "pct_unaffiliated": pct_unaff,
                "pct_rep":         pct_rep,
            },
        })

    out_fc = {"type": "FeatureCollection", "features": output_features}
    OUTPUT_PATH.write_text(json.dumps(out_fc))

    matched = sum(1 for f in output_features if f["properties"]["pct_dem"] is not None)
    print(f"\nMunicipalities in NJ-07: {len(output_features)}")
    print(f"Matched to VOTER_REG:    {matched}/{len(output_features)}")

    if unmatched:
        print("\nUnmatched — add these keys to VOTER_REG (with actual dem/unaff/total counts):")
        for key in sorted(set(unmatched)):
            print(f"  {key}: (dem_count, unaff_count, total_count),")

    print(f"\nOutput written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
