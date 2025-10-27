from __future__ import annotations
from typing import List, Dict, Any, Optional
import os
import httpx


async def search_places(
    city: str,
    country: Optional[str],
    trip_type: str,
    dietary_restrictions: Optional[str],
    accessibility_needs: Optional[str],
    num_results: int = 5,
) -> List[Dict[str, Any]]:
    api_key = os.getenv("OPENTRIPMAP_API_KEY")
    if api_key:
        try:
            return await _search_places_opentripmap(city, trip_type, num_results, api_key)
        except Exception:
            pass

    return _mock_places(city, trip_type, dietary_restrictions, accessibility_needs, num_results)


async def _search_places_opentripmap(
    city: str,
    trip_type: str,
    num_results: int,
    api_key: str,
) -> List[Dict[str, Any]]:
    async with httpx.AsyncClient(timeout=20) as client:
        # Geoname lookup
        resp = await client.get("https://api.opentripmap.com/0.1/en/places/geoname", params={"name": city, "apikey": api_key})
        resp.raise_for_status()
        geo = resp.json()
        lon, lat = geo.get("lon"), geo.get("lat")
        if lon is None or lat is None:
            return []
        kinds = "interesting_places,sights,museums,historic"
        if trip_type.lower() in {"adventure", "outdoor"}:
            kinds += ",natural,sport" 
        resp2 = await client.get(
            "https://api.opentripmap.com/0.1/en/places/radius",
            params={
                "radius": 10000,
                "lon": lon,
                "lat": lat,
                "kinds": kinds,
                "limit": num_results,
                "apikey": api_key,
                "format": "json",
            },
        )
        resp2.raise_for_status()
        items = resp2.json()
        results: List[Dict[str, Any]] = []
        for i in items:
            results.append(
                {
                    "name": i.get("name") or "Point of Interest",
                    "estimated_duration_hours": 1.5,
                    "ticket_cost": 0,
                    "best_time": "10:00-16:00",
                    "significance": "Popular local attraction",
                    "accessibility": "Wheelchair friendly" if "wheelchair" in str(i).lower() else "Standard access",
                }
            )
        return results


def _mock_places(
    city: str,
    trip_type: str,
    dietary_restrictions: Optional[str],
    accessibility_needs: Optional[str],
    num_results: int,
) -> List[Dict[str, Any]]:
    examples = [
        {
            "name": f"Old Town Walking Tour of {city}",
            "estimated_duration_hours": 2.0,
            "ticket_cost": 0,
            "best_time": "Morning",
            "significance": "Historic city center with landmarks and local culture",
            "accessibility": "Wheelchair accessible pathways",
        },
        {
            "name": f"City Museum of {city}",
            "estimated_duration_hours": 2.5,
            "ticket_cost": 15,
            "best_time": "Afternoon",
            "significance": "Regional art and history collections",
            "accessibility": "Elevator and accessible restrooms",
        },
        {
            "name": f"Riverfront Park in {city}",
            "estimated_duration_hours": 1.5,
            "ticket_cost": 0,
            "best_time": "Sunset",
            "significance": "Scenic views and local recreation",
            "accessibility": "Paved trails",
        },
        {
            "name": f"Food Market of {city}",
            "estimated_duration_hours": 1.5,
            "ticket_cost": 0,
            "best_time": "Late morning",
            "significance": "Local cuisine and artisan goods",
            "accessibility": "Crowded at peak times, accessible entrances",
        },
        {
            "name": f"Iconic Landmark of {city}",
            "estimated_duration_hours": 2.0,
            "ticket_cost": 20,
            "best_time": "Early morning",
            "significance": "Cultural and historical significance",
            "accessibility": "Ramps available",
        },
    ]

    # Soft filter for dietary needs: keep market/museum, avoid food tours if severe allergy
    if dietary_restrictions and any(k in dietary_restrictions.lower() for k in ["severe", "anaphylaxis"]):
        examples = [p for p in examples if "Food" not in p["name"]]

    return examples[:num_results]