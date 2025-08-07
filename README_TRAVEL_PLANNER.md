# Travel Planner (FastAPI)

Run a lightweight backend that provides a questionnaire and personalized recommendations. Real-time APIs are used when keys are provided; otherwise, mock data is used.

## Quick start

1. Create and activate a virtualenv (optional)
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables (optional for real-time data):

Copy `.env.example` to `.env` and fill in keys. Or export variables directly.

4. Start the server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` in your browser.

## Environment variables
- `KIWI_TEQUILA_API_KEY`: Flight search via Kiwi Tequila API
- `AMADEUS_CLIENT_ID`, `AMADEUS_CLIENT_SECRET`: Flight/Hotel search via Amadeus (placeholder in scaffold)
- `OPENTRIPMAP_API_KEY`: Attractions and POIs

## Notes
- If no API keys are provided, the app returns realistic mock data for development.
- Budget breakdown includes flights, accommodation, activities, and food, with cost-saving tips.
- Warnings include budget overages, advisories, group size/age suitability, dietary and accessibility considerations.