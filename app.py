from fastapi import FastAPI, Query
from typing import List, Optional, Dict
from pydantic import BaseModel
from scraper import Info


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
    version="0.1.0",
)

scraper = Info()


@app.get("/stations", response_model=Dict[str, Station])
def get_stations(
    lat: str = Query("50.94280233052442", description="Latitude"),
    lon: str = Query("6.941247823375725", description="Longitude"),
    distance: int = Query(10, description="Search radius in km"),
    fuelType: str = Query("Super", description="Fuel type, e.g. 'Super', 'Super E10', 'Diesel'"),
    sort: str = Query("PRICE_ASC", description="Sort the data")
):
    stations = scraper.get_fuelstations(distance=distance, lon=lon, lat=lat, fuel_type=fuelType, sort=sort)
    return stations