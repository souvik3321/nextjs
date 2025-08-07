from __future__ import annotations
from typing import Dict, Any, Optional
import httpx


async def fetch_travel_advisories(city: str, country: Optional[str]) -> Dict[str, Any]:
    # Try fetching global advisory via travel-advisory.info if country code present; otherwise return generic note.
    if country and len(country) == 2:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get("https://www.travel-advisory.info/api", params={"countrycode": country.upper()})
                resp.raise_for_status()
                data = resp.json()
                entry = data.get("data", {}).get(country.upper(), {}).get("advisory", {})
                return {
                    "score": entry.get("score"),
                    "message": entry.get("message"),
                    "source": entry.get("source"),
                }
        except Exception:
            pass

    return {
        "score": None,
        "message": "Verify any current travel restrictions or health advisories for your destination via official sources.",
        "source": "manual",
    }