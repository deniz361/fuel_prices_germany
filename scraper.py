import requests
import brotli
import re
import json
from bs4 import BeautifulSoup



class Info():
    def __init__(self):
        self.url = "https://www.adac.de/verkehr/tanken-kraftstoff-antrieb/kraftstoffpreise/"

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Mode": "navigate",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0.1 Safari/605.1.15",
            "Accept-Encoding": "identity",
            "Referer": "https://www.adac.de/verkehr/tanken-kraftstoff-antrieb/?redirectId=quer.vpo.tanken",
            "Priority": "u=0, i",
        }
        
    def get_fuelstations(self, distance, lat, lon, fuel_type, sort):
        params = {
            "distance": distance,
            "lat": lat,
            "lon": lon,
            "fuelType": fuel_type,
            "sort": sort
        }

        response = requests.get(self.url, params=params, headers=self.headers)

        if response.headers.get("Content-Encoding") == "br":
            html = brotli.decompress(response.content).decode("utf-8")
        else:
            html = response.text


        soup = BeautifulSoup(html, "html.parser")

        # Find ALL <script> tags
        scripts = soup.find_all("script")

        json_data = None

        # Try to locate the script tag with embedded JSON
        for s in scripts:
            if s.string and "FuelStation" in s.string:

                # Clean trailing semicolon or window.var = prefix
                raw = s.string.strip()
                
                raw = raw.replace("window.__APOLLO_STATE__=", "")

                # remove everything after the last }
                raw = re.sub(r'}\s*[^}]*$', '}', raw)
                
                data = json.loads(raw)
                
                # Nur FuelStation-Einträge rausfiltern
                stations_raw = {
                    k: v
                    for k, v in data.items()
                    if k.startswith("FuelStation:")
                }
                
                json_data = stations_raw

        if not json_data:
            raise Exception("Could not find JSON with FuelStation data.")


        print("Found", len(json_data), "stations")

        # Print each result cleanly
        # for station_id, info in json_data.items():
        #     print(station_id, info)
            
        return json_data
    
if __name__ == "__main__":
    info = Info()
    
    info.get_fuelstations(10, "50.94280233052442", "6.941247823375725", "Super", "PRICE_ASC")
