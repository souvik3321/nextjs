from __future__ import annotations
from typing import Dict, Any, List


def build_budget_breakdown(
    flights: List[dict],
    hotels: List[dict],
    places: List[dict],
    num_travelers: int,
    nights: int,
    currency: str,
) -> Dict[str, Any]:
    flight_per_person = flights[0]["price"] if flights else 0
    flight_total = flight_per_person * num_travelers

    hotel_per_night = hotels[0]["price_per_night"] if hotels else 0
    hotel_total = hotel_per_night * nights

    activities_total = int(sum(p.get("ticket_cost", 0) for p in places))

    # Food estimate per person per day (simple heuristic)
    food_per_person_per_day = 45
    food_total = food_per_person_per_day * num_travelers * max(1, nights)

    estimated_total = flight_total + hotel_total + activities_total + food_total

    tips: List[str] = []
    if flights and flights[-1]["price"] < flights[0]["price"]:
        tips.append("Consider the slightly longer/layover flight to save on airfare.")
    if hotels and hotels[-1]["price_per_night"] < hotels[0]["price_per_night"]:
        tips.append("Choose a hotel a bit farther from the center to reduce nightly rates.")
    if activities_total > 0:
        tips.append("Look for combo tickets or city passes to reduce attraction costs.")
    tips.append("Travel with carry-on only to avoid checked baggage fees where possible.")

    return {
        "currency": currency,
        "estimated_total": round(estimated_total, 2),
        "by_category": {
            "flights": {"amount": round(flight_total, 2), "currency": currency},
            "accommodation": {"amount": round(hotel_total, 2), "currency": currency},
            "activities": {"amount": round(activities_total, 2), "currency": currency},
            "food": {"amount": round(food_total, 2), "currency": currency},
        },
        "tips": tips,
    }