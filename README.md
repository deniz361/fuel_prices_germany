# German Fuel Prices API – Real-Time Gas Station Data

Retrieve **live fuel prices** for gas stations across **Germany**, including Super (E5), Super E10, Diesel.  
Perfect for apps, dashboards, route planners, mobility platforms and AI agents that need **accurate, real-time fuel data**.

## Features
- **Real-time fuel prices**
- Search by **latitude, longitude & radius (km)**
- Covers **all gas stations in Germany**
- Data refreshed frequently
- Ideal for:
  - Fuel price comparison apps  
  - “Cheapest gas near me” tools  
  - Navigation & routing systems  
  - Fleet management  
  - Smart mobility & logistics  
  - AI assistants & automation  

## Supported Cities
Works everywhere in Germany, including:  
**Berlin, Hamburg, Munich (München), Cologne (Köln), Frankfurt, Stuttgart, Düsseldorf, Dortmund, Leipzig, Hannover**, and all other regions.

## Returned Data
Each station response includes:

| Field | Type  |Description |
|-------|-------|-------------|
| `id` |int|Unique station ID |
| `price` |float|Current fuel price |
| `fuelType` |String| Super E5, Super E10, Diesel|
| `updatedAt` |int| Time of last update in Unix format |
| `street` |String| Street name |
| `zipcode` |String| Postal code |
| `city` |String| City |
| `operator` |String| Brand / fuel operator |
| `lat` |float| Latitude |
| `lon` |float| Longitude |
| `timeUntilClosing` |int| Minutes until closing (`-1` = open 24h) |

## Endpoint: Get Fuel Stations

### GET `/stations`

### Query Parameters

| Parameter | Type | Required | Description |
|----------|------|----------|-------------|
| `lat` | float | ✔ | Latitude of search center |
| `lon` | float | ✔ | Longitude of search center |
| `distance` | int | ❌ | Search radius (km), default: `10` |
| `fuelType` | String | ❌ | Default: `Super` |
| `sort` | String | ❌ | Default: `PRICE_ASC` |

## Example Request (cURL)
```bash
curl -X GET "https://fuelpricesgermany-production.up.railway.app/stations?lat=50.9428&lon=6.9412&distance=10&fuelType=Super"
```

## Example Response
```json
{
   "data":[
      {
         "global_id":1237975,
         "price":1.648,
         "fuelType":"Super E5",
         "updatedAt":1763564280,
         "street":"Max-Planck Straße 9",
         "zipcode":"50858",
         "city":"Köln-Marsdorf",
         "operator":"Globus SB Warenhaus",
         "lat":50.921451568603516,
         "lon":6.853320121765137,
         "timeUntilClosing":-1
      },
      {
         "global_id":1236767,
         "price":1.649,
         "fuelType":"Super E5",
         "updatedAt":1763564400,
         "street":"Dellbrücker Hauptstraße 9",
         "zipcode":"51069",
         "city":"Koeln",
         "operator":"SB",
         "lat":50.9734001159668,
         "lon":7.075281143188477,
         "timeUntilClosing":353
      }
   ]
}
```

## Use Cases
- Mobile “cheap fuel finder”
- Car navigation/map integrations
- EV/hybrid fuel cost estimation
- Fleet management dashboards
- Logistics routing optimization
- Travel cost calculators
- AI assistants needing fuel data


## Disclaimer
This API provides fuel price data sourced from publicly accessible information.  
Not affiliated with any fuel provider.  
Use responsibly and in compliance with local data laws.

## Need help?
If you need:
- Custom features  
- Higher rate limits  
- European-wide fuel data  
- More endpoints  

Just message me through RapidAPI or open an issue in the GitHub repository.
