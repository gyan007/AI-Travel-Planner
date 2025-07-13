from datetime import datetime
from typing import List, Dict

def calculate_days(start_date: str, end_date: str) -> int:
    try:
        d1 = datetime.strptime(start_date, "%Y-%m-%d")
        d2 = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        try:
            d1 = datetime.strptime(start_date, "%d-%m-%Y")
            d2 = datetime.strptime(end_date, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY.")
    return max((d2 - d1).days + 1, 1)


def estimate_budget(
    days: int,
    hotels: List[Dict],
    food_cost_per_day: float = 500,
    transport_cost_per_km: float = 10,
    travel_distance_km: float = 0.0
) -> Dict:
    hotel_prices = []
    for hotel in hotels:
        if hotel["price"].count("₹") > 0:
            hotel_prices.append(len(hotel["price"]) * 1000)
        else:
            hotel_prices.append(2000)
    avg_hotel_cost = sum(hotel_prices) / len(hotel_prices) if hotel_prices else 2500
    total_hotel_cost = avg_hotel_cost * days
    total_food_cost = food_cost_per_day * days
    total_transport_cost = travel_distance_km * transport_cost_per_km
    total = total_hotel_cost + total_food_cost + total_transport_cost
    return {
        "hotel_per_night": round(avg_hotel_cost, 2),
        "total_hotel": round(total_hotel_cost, 2),
        "total_food": round(total_food_cost, 2),
        "total_transport": round(total_transport_cost, 2),
        "total_budget_estimate": round(total, 2)
    }
