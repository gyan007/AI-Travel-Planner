import requests
from typing import Dict

OSRM_BASE_URL = "http://router.project-osrm.org/route/v1"

import requests

def get_route(start_lat, start_lon, end_lat, end_lon, mode="car"):
    try:
        url = f"http://router.project-osrm.org/route/v1/{mode}/{start_lon},{start_lat};{end_lon},{end_lat}"
        params = {
            "overview": "full",
            "geometries": "geojson",
            "steps": "true",          
            "annotations": "true"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("code") != "Ok" or not data.get("routes"):
            return {"error": "No valid route found"}

        route = data["routes"][0]
        distance_km = round(route["distance"] / 1000, 2)
        duration_min = round(route["duration"] / 60, 2)


        steps = []
        for leg in route.get("legs", []):
            for step in leg.get("steps", []):
                maneuver = step.get("maneuver", {})
                instruction = f"{maneuver.get('type', '').capitalize()} {step.get('name', '')}".strip()
                if maneuver.get("modifier"):
                    instruction += f" and turn {maneuver['modifier']}"
                steps.append(instruction)

        return {
            "distance_km": distance_km,
            "duration_min": duration_min,
            "steps": steps or ["No step-by-step instructions available."]
        }

    except Exception as e:
        return {"error": str(e)}
