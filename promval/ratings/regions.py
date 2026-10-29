"""Event host country codes mapped to the four competitive macro regions."""

REGION_CODES = {
    "Americas": "us ca mx br ar cl co pe uy ve py bo ec cr gt pa pr do na latam".split(),
    "EMEA": (
        "eu gb de fr es it pt nl be se no dk fi pl cz at ch tr ru ua by kz sa ae "
        "eg ma za il gr ro hu rs hr bg ie lt lv ee me mena cis"
    ).split(),
    "Pacific": "kr jp ph id th vn sg my au nz in tw hk mo kh mm pk bd lk np mn".split(),
    "China": ["cn"],
}
# VLR country code sa is Saudi Arabia (EMEA). Explicit South America aliases
# avoid interpreting that country flag as a continental abbreviation.
REGION_CODES["Americas"] += [
    "south-america",
    "south_america",
    "north-america",
    "north_america",
]
COUNTRY_REGION = {
    code: region for region, codes in REGION_CODES.items() for code in codes
}


def macro_region(code):
    return COUNTRY_REGION.get(str(code).strip().lower())
