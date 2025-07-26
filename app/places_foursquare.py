import requests
from typing import List

FOURSQUARE_API_KEY = "Your_Foursquare_API_Key"  
BASE_URL = "https://api.foursquare.com/v3/places/search"

HEADERS = {
    "Authorization": FOURSQUARE_API_KEY,
    "Accept": "application/json"
}

CATEGORY_MAP = {
    "hotels": "19014",        
    "restaurants": "13065", 
}

def search_foursquare_businesses(lat: float, lon: float, categories: List[str], limit=5):
    results = []

    for category in categories:
        category_id = CATEGORY_MAP.get(category)
        if not category_id:
            continue

        params = {
            "ll": f"{lat},{lon}",
            "limit": limit,
            "radius": 5000,
            "categories": category_id,
            "sort": "RELEVANCE"
        }

        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        for place in data.get("results", []):
            results.append({
                "name": place.get("name"),
                "category": category,
                "rating": "N/A", 
                "price": "₹₹",   
                "address": ", ".join(place["location"].get("formatted_address", [])),
                "phone": place.get("tel", ""),
                "url": f"https://foursquare.com/v/{place['fsq_id']}"
            })

    return results
