from __future__ import annotations
from typing import List, Dict, Any
from app.main import TripRequest


def validate_recommendations(
    trip: TripRequest,
    flights: List[Dict[str, Any]],
    hotels: List[Dict[str, Any]],
    places: List[Dict[str, Any]],
    advisories: Dict[str, Any],
    budget: Dict[str, Any],
) -> List[str]:
    warnings: List[str] = []

    # Budget check
    if trip.max_budget is not None and budget.get("estimated_total", 0) > trip.max_budget:
        warnings.append(
            f"Estimated total {budget['estimated_total']} {budget['currency']} exceeds your max budget of {trip.max_budget} {trip.budget_currency}."
        )

    # Advisory check
    if advisories.get("score") and float(advisories.get("score")) >= 3.0:
        warnings.append("Destination currently has elevated travel advisories. Review guidance before booking.")

    # Group size and age
    if trip.num_travelers >= 6:
        warnings.append("Large group detected; consider booking group accommodations or apartments.")
    if trip.traveler_ages and any(x in trip.traveler_ages.lower() for x in ["infant", "baby", "child"]):
        warnings.append("Traveling with children: verify crib availability and child-friendly attractions.")

    # Dietary restrictions
    if trip.dietary_restrictions:
        warnings.append("Verify dietary options with airlines and hotels; carry translation cards if needed.")

    # Accessibility
    if trip.accessibility_needs:
        warnings.append("Confirm step-free access and accessible bathrooms at selected hotels and attractions.")

    return warnings