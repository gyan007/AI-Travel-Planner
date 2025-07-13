import requests
from typing import List

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

HEADERS = {
    "User-Agent": "AI Travel Planner"
}

def get_coordinates(location: str):
    params = {"q": location, "format": "json"}
    response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])


OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def get_pois(lat: float, lon: float, keywords: List[str]):
    search_tags = keywords or ["viewpoint", "museum", "attraction", "park", "monument"]

    query = f"""
    [out:json];
    (
    {"".join([
        f'node["tourism"="{tag}"](around:5000,{lat},{lon});'
        f'way["tourism"="{tag}"](around:5000,{lat},{lon});'
        f'relation["tourism"="{tag}"](around:5000,{lat},{lon});'
        f'node["leisure"="{tag}"](around:5000,{lat},{lon});'
        f'way["leisure"="{tag}"](around:5000,{lat},{lon});'
        f'relation["leisure"="{tag}"](around:5000,{lat},{lon});'
        f'node["amenity"="{tag}"](around:5000,{lat},{lon});'
        f'way["amenity"="{tag}"](around:5000,{lat},{lon});'
        f'relation["amenity"="{tag}"](around:5000,{lat},{lon});'
        for tag in search_tags
    ])}
    );
    out center;
    """

    try:
        response = requests.post(OVERPASS_URL, data=query.encode("utf-8"), timeout=20)
        response.raise_for_status()
        data = response.json()

        pois = []
        for el in data.get("elements", []):
            tags = el.get("tags", {})
            name = tags.get("name") or tags.get("alt_name") or tags.get("official_name") or "Unnamed Place"
            type_ = tags.get("tourism") or tags.get("leisure") or tags.get("amenity") or "N/A"
            lat_res = el.get("lat") or el.get("center", {}).get("lat")
            lon_res = el.get("lon") or el.get("center", {}).get("lon")

            if lat_res and lon_res:
                pois.append({
                    "name": name,
                    "type": type_,
                    "lat": lat_res,
                    "lon": lon_res,
                })

        return pois
    except Exception as e:
        print(f"[get_pois] Error: {e}")
        return []

