from __future__ import annotations
from datetime import date
from typing import List, Dict, Any
import os
import httpx


async def search_flights(
    origin_city: str,
    destination_city: str,
    start_date: date,
    end_date: date,
    num_travelers: int,
    currency: str = "USD",
) -> List[Dict[str, Any]]:
    """Return top flight options. Attempts real APIs if keys present; falls back to mock.
    Each flight dict includes: price, duration, airline, layovers, total_travel_time, booking_url.
    """
    # Future: resolve IATA codes from city names using Amadeus locations or Kiwi locations
    tequila_key = os.getenv("KIWI_TEQUILA_API_KEY")
    amadeus_key = os.getenv("AMADEUS_CLIENT_ID")
    amadeus_secret = os.getenv("AMADEUS_CLIENT_SECRET")

    if tequila_key:
        try:
            return await _search_flights_tequila(
                origin_city, destination_city, start_date, end_date, num_travelers, currency, tequila_key
            )
        except Exception:
            pass

    if amadeus_key and amadeus_secret:
        try:
            return await _search_flights_amadeus(
                origin_city, destination_city, start_date, end_date, num_travelers, currency, amadeus_key, amadeus_secret
            )
        except Exception:
            pass

    return _mock_flights(origin_city, destination_city, start_date, end_date, num_travelers, currency)


async def _search_flights_tequila(
    origin_city: str,
    destination_city: str,
    start_date: date,
    end_date: date,
    num_travelers: int,
    currency: str,
    api_key: str,
) -> List[Dict[str, Any]]:
    # Minimal example using Tequila API; in production resolve city->IATA
    headers = {"apikey": api_key}
    params = {
        "fly_from": origin_city,
        "fly_to": destination_city,
        "date_from": start_date.strftime("%d/%m/%Y"),
        "date_to": start_date.strftime("%d/%m/%Y"),
        "return_from": end_date.strftime("%d/%m/%Y"),
        "return_to": end_date.strftime("%d/%m/%Y"),
        "curr": currency,
        "adults": num_travelers,
        "limit": 5,
        "sort": "price",
    }
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get("https://api.tequila.kiwi.com/v2/search", headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for r in data.get("data", [])[:5]:
            results.append(
                {
                    "price": r.get("price"),
                    "currency": currency,
                    "duration": r.get("fly_duration"),
                    "airline": ", ".join(r.get("airlines", [])),
                    "layovers": [s.get("cityTo") for s in r.get("route", []) if s.get("cityTo") not in (destination_city,)],
                    "total_travel_time": r.get("duration", {}).get("total"),
                    "booking_url": r.get("deep_link"),
                }
            )
        return results


async def _search_flights_amadeus(
    origin_city: str,
    destination_city: str,
    start_date: date,
    end_date: date,
    num_travelers: int,
    currency: str,
    client_id: str,
    client_secret: str,
) -> List[Dict[str, Any]]:
    # Placeholder; Amadeus requires token then flight-offers. For brevity, return empty to trigger mock.
    raise RuntimeError("Amadeus integration not configured in this scaffold")


def _mock_flights(
    origin_city: str,
    destination_city: str,
    start_date: date,
    end_date: date,
    num_travelers: int,
    currency: str,
) -> List[Dict[str, Any]]:
    base_prices = [350, 420, 480, 510, 590]
    airlines = ["SkyJet", "AeroLine", "Continental Wings", "BlueAir", "EuroFly"]
    durations = ["9h 45m", "10h 20m", "11h 05m", "12h 10m", "8h 55m"]
    layovers_list = [["Reykjavik"], ["Frankfurt"], ["Paris"], ["Dubai"], []]
    total_times = [585, 620, 665, 730, 535]

    results = []
    for i in range(5):
        results.append(
            {
                "price": base_prices[i],
                "currency": currency,
                "duration": durations[i],
                "airline": airlines[i],
                "layovers": layovers_list[i],
                "total_travel_time": total_times[i],
                "booking_url": None,
            }
        )
    return results