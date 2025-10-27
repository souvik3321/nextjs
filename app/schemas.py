from __future__ import annotations
from datetime import date
from typing import Optional
from pydantic import BaseModel, field_validator


class TripRequest(BaseModel):
    destination_city: str
    destination_country: Optional[str] = None
    base_location_city: str
    base_location_country: Optional[str] = None
    start_date: date
    end_date: date
    num_travelers: int
    trip_type: str
    dietary_restrictions: Optional[str] = None
    budget_currency: str = "USD"
    max_budget: Optional[float] = None
    accessibility_needs: Optional[str] = None
    traveler_ages: Optional[str] = None

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v: date, info):
        start = info.data.get("start_date")
        if start and v < start:
            raise ValueError("End date must be on or after start date")
        return v