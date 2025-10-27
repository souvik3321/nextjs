from datetime import date, datetime
from typing import Optional, List, Dict, Any
import os

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv

from app.services.flight_service import search_flights
from app.services.hotel_service import search_hotels
from app.services.places_service import search_places
from app.services.budget_service import build_budget_breakdown
from app.services.advisory_service import fetch_travel_advisories
from app.services.validation_service import validate_recommendations
from app.schemas import TripRequest

load_dotenv()

app = FastAPI(title="Travel Planner", version="0.1.0")

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
templates_dir = os.path.join(current_dir, "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/plan", response_class=HTMLResponse)
async def plan_trip(
    request: Request,
    destination_city: str = Form(...),
    destination_country: str = Form(""),
    base_location_city: str = Form(...),
    base_location_country: str = Form(""),
    start_date: str = Form(...),
    end_date: str = Form(...),
    num_travelers: int = Form(...),
    trip_type: str = Form(...),
    dietary_restrictions: str = Form(""),
    budget_currency: str = Form("USD"),
    max_budget: float = Form(0),
    accessibility_needs: str = Form(""),
    traveler_ages: str = Form(""),
):
    trip = TripRequest(
        destination_city=destination_city.strip(),
        destination_country=destination_country.strip() or None,
        base_location_city=base_location_city.strip(),
        base_location_country=base_location_country.strip() or None,
        start_date=datetime.fromisoformat(start_date).date(),
        end_date=datetime.fromisoformat(end_date).date(),
        num_travelers=num_travelers,
        trip_type=trip_type,
        dietary_restrictions=dietary_restrictions or None,
        budget_currency=budget_currency,
        max_budget=max_budget or None,
        accessibility_needs=accessibility_needs or None,
        traveler_ages=traveler_ages or None,
    )

    nights = (trip.end_date - trip.start_date).days or 1

    flights = await search_flights(
        origin_city=trip.base_location_city,
        destination_city=trip.destination_city,
        start_date=trip.start_date,
        end_date=trip.end_date,
        num_travelers=trip.num_travelers,
        currency=trip.budget_currency,
    )

    hotels = await search_hotels(
        city=trip.destination_city,
        start_date=trip.start_date,
        end_date=trip.end_date,
        num_guests=trip.num_travelers,
        currency=trip.budget_currency,
        trip_type=trip.trip_type,
    )

    places = await search_places(
        city=trip.destination_city,
        country=trip.destination_country,
        trip_type=trip.trip_type,
        dietary_restrictions=trip.dietary_restrictions,
        accessibility_needs=trip.accessibility_needs,
        num_results=5,
    )

    advisories = await fetch_travel_advisories(
        city=trip.destination_city, country=trip.destination_country
    )

    budget = build_budget_breakdown(
        flights=flights,
        hotels=hotels,
        places=places,
        num_travelers=trip.num_travelers,
        nights=nights,
        currency=trip.budget_currency,
    )

    warnings = validate_recommendations(
        trip=trip,
        flights=flights,
        hotels=hotels,
        places=places,
        advisories=advisories,
        budget=budget,
    )

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "trip": trip,
            "flights": flights[:5],
            "hotels": hotels[:5],
            "places": places[:5],
            "advisories": advisories,
            "budget": budget,
            "warnings": warnings,
        },
    )