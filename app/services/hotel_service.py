from __future__ import annotations
from datetime import date
from typing import List, Dict, Any
import os
import httpx


async def search_hotels(
    city: str,
    start_date: date,
    end_date: date,
    num_guests: int,
    currency: str,
    trip_type: str,
) -> List[Dict[str, Any]]:
    amadeus_key = os.getenv("AMADEUS_CLIENT_ID")
    amadeus_secret = os.getenv("AMADEUS_CLIENT_SECRET")

    if amadeus_key and amadeus_secret:
        try:
            return await _search_hotels_amadeus(city, start_date, end_date, num_guests, currency, amadeus_key, amadeus_secret)
        except Exception:
            pass

    return _mock_hotels(city, start_date, end_date, num_guests, currency, trip_type)


async def _search_hotels_amadeus(
    city: str,
    start_date: date,
    end_date: date,
    num_guests: int,
    currency: str,
    client_id: str,
    client_secret: str,
) -> List[Dict[str, Any]]:
    # Placeholder; Amadeus Hotel Search requires token then hotel-offers
    raise RuntimeError("Amadeus integration not configured in this scaffold")


def _mock_hotels(
    city: str,
    start_date: date,
    end_date: date,
    num_guests: int,
    currency: str,
    trip_type: str,
) -> List[Dict[str, Any]]:
    hotels = [
        {
            "name": "Central Plaza Hotel",
            "price_per_night": 120,
            "currency": currency,
            "location_rating": 9.2,
            "amenities": ["Free WiFi", "Breakfast", "Gym"],
            "user_reviews": 1842,
            "proximity": "0.5 km to city center",
            "accessibility": ["Elevator", "Wheelchair accessible"],
        },
        {
            "name": "Riverside Boutique",
            "price_per_night": 95,
            "currency": currency,
            "location_rating": 8.7,
            "amenities": ["Free WiFi", "Bar", "Pet-friendly"],
            "user_reviews": 968,
            "proximity": "1.2 km to main station",
            "accessibility": ["Ground-floor rooms"],
        },
        {
            "name": "Grand Continental",
            "price_per_night": 160,
            "currency": currency,
            "location_rating": 9.0,
            "amenities": ["Pool", "Spa", "Executive lounge"],
            "user_reviews": 2560,
            "proximity": "Adjacent to convention center",
            "accessibility": ["Accessible parking", "Hearing assistance"],
        },
        {
            "name": "City Stay Inn",
            "price_per_night": 75,
            "currency": currency,
            "location_rating": 8.1,
            "amenities": ["Kitchenette", "Laundry"],
            "user_reviews": 421,
            "proximity": "2.3 km to old town",
            "accessibility": ["Wheelchair accessible"],
        },
        {
            "name": "Art House Hotel",
            "price_per_night": 110,
            "currency": currency,
            "location_rating": 8.9,
            "amenities": ["Rooftop terrace", "Restaurant"],
            "user_reviews": 1333,
            "proximity": "0.8 km to museum district",
            "accessibility": ["Elevator"],
        },
    ]
    return hotels