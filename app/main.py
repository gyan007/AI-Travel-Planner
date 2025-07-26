from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from app.places import get_coordinates, get_pois
from app.weather import get_weather_forecast
from app.routes import get_route
from app.budget import calculate_days, estimate_budget
from app.places_foursquare import search_foursquare_businesses

app = FastAPI(title="AI Travel Planner", version="1.0.0")


class TravelRequest(BaseModel):
    source: str
    destination: str
    start_date: str
    end_date: str
    preferences: List[str]
    budget: Optional[float] = None
    transport_mode: Optional[str] = "car"



@app.post("/plan")
def plan_trip(request: TravelRequest):
    try:
        # Get coordinates
        source_coords = get_coordinates(request.source)
        dest_coords = get_coordinates(request.destination)

        if not source_coords or not dest_coords:
            return {"error": "Source or destination location not found"}

        source_lat, source_lon = source_coords
        dest_lat, dest_lon = dest_coords

        # Get POIs & weather at destination
        pois = get_pois(dest_lat, dest_lon, request.preferences)
        weather = get_weather_forecast(dest_lat, dest_lon)

        # Foursquare places
        foursquare_categories = []
        if "food" in request.preferences:
            foursquare_categories.append("restaurants")
        if "hotel" in request.preferences:
            foursquare_categories.append("hotel")

        places = search_foursquare_businesses(dest_lat, dest_lon, foursquare_categories)
        hotel_data = [p for p in places if p["category"] == "hotel"]

        # Route
        # Fetch route
        route_result = get_route(
            start_lat=source_lat,
            start_lon=source_lon,
            end_lat=dest_lat,
            end_lon=dest_lon,
            mode=request.transport_mode or "car"
        )
        
        days = calculate_days(request.start_date, request.end_date)
        
        # Handle route fetch failure gracefully
        if "error" in route_result:
            route_result = {
                "distance_km": 10 * days,
                "duration_min": 60 * days,
                "steps": ["Route unavailable. Please check manually using the below option."]
            }
        else:
            total_distance = max(route_result["distance_km"], 10 * days)

        # Budget estimate
        budget = estimate_budget(days, hotel_data, travel_distance_km=total_distance)

        return {
            "source": request.source,
            "destination": request.destination,
            "source_coordinates": {"lat": source_lat, "lon": source_lon},
            "destination_coordinates": {"lat": dest_lat, "lon": dest_lon},
            "weather": weather,
            "places": pois[:10],
            "recommendations": places,
            "budget": budget,
            "route": route_result
        }

    except Exception as e:
        return {"error": str(e)}



@app.get("/route")
def plan_route(
    start_lat: float = Query(...),
    start_lon: float = Query(...),
    end_lat: float = Query(...),
    end_lon: float = Query(...),
    mode: str = "car"
):
    return get_route(start_lat, start_lon, end_lat, end_lon, mode)
