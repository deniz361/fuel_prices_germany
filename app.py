from fastapi import FastAPI, Query, Response, HTTPException
from typing import List, Optional, Dict
from pydantic import BaseModel
from scraper import Info
import json

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class Station(BaseModel):
    id: Optional[str]
    price: Optional[str]
    fuelType: Optional[str]
    fuelTypeUpdatedAt: Optional[str]
    street: Optional[str]
    zipcode: Optional[str]
    city: Optional[str]
    operator: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    timeUntilClosing: Optional[int]
    permaLink: Optional[str]
    
    
app = FastAPI(
    title="ADAC Fuel Scraper API",
    description="Unofficial API that returns nearby fuel prices based on ADAC website.",
    version="0.1.0"
)

scraper = Info()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error": "INVALID_REQUEST",
            "message": "You must provide both 'lat' and 'lon' as query parameters.",
        }
    )

@app.get("/stations", response_model=Dict[str, Station])
def get_stations(
    lat: float = Query(description="Latitude"),
    lon: float = Query(description="Longitude"),
    distance: int = Query(10, description="Search radius in km"),
    fuelType: str = Query("Super", description="Fuel type, e.g. 'Super', 'Super E10', 'Diesel'"),
    sort: str = Query("PRICE_ASC", description="Sort the data, e.g. 'PRICE_ASC', 'PRICE_DESC'")
):  
    # trying to scrape the data
    try:
        stations = scraper.get_fuelstations(distance=distance, lon=lon, lat=lat, fuel_type=fuelType, sort=sort)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
    
    return Response(
        content=json.dumps(stations, ensure_ascii=False),
        media_type="application/json; charset=utf-8",
    )