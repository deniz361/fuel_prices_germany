import requests
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


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
        
        self.offsets = {
            "Heute": 0,
            "Gestern": -1
        }
        
    def convert_timestamp(self, time):
        ts = time.strip()
        if "," in ts:
            head, time_str = [x.strip() for x in ts.split(",", 1)]

        if head in self.offsets and time_str:
            offset = self.offsets[head]
        base_date = datetime.now() + timedelta(days=offset)
        time_obj = datetime.strptime(time_str, "%H:%M")

        merged = datetime(
            year=base_date.year,
            month=base_date.month,
            day=base_date.day,
            hour=time_obj.hour,
            minute=time_obj.minute
        )
        return int(merged.timestamp())

        
    def format_data(self, json_data):
        json_list = []
        
        for entry in json_data:
            
            section = {}
            raw = json_data[entry]
            
            section["global_id"] = int(raw["id"])
            section["price"] = float(raw["price"].replace(",", "."))
            section["fuelType"] = raw["fuelType"]
            
                
            last_updated = self.convert_timestamp(raw["fuelTypeUpdatedAt"])
            section["updatedAt"] = last_updated
            section["street"] = raw["street"]
            section["zipcode"] = raw["zipcode"]
            section["city"] = raw["city"]
            section["operator"] = raw["operator"]
            section["lat"] = raw["lat"]
            section["lon"] = raw["lon"]
            section["timeUntilClosing"] = raw["timeUntilClosing"]
            
            json_list.append(section)
            
        json_object = {} 
        json_object["data"] = json_list
        
        return json_object
        
    def get_fuelstations(self, lat, lon, distance, fuel_type, sort):
        params = {
            "distance": distance,
            "lat": lat,
            "lon": lon,
            "fuelType": fuel_type,
            "sort": sort
        }
        
        response = requests.get(self.url, headers=self.headers, params=params)
        response.encoding = response.apparent_encoding or "utf-8"
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
                
                # stations_raw = {}
                
                # for k, v in data.items():
                #     if k.startswith("FuelStations:"):
                #         stations_raw[k] = v
                        
                # Nur FuelStation-Einträge rausfiltern
                stations_raw = {
                    k: v
                    for k, v in data.items()
                    if k.startswith("FuelStation:")
                }
                
                json_data = stations_raw

        if not json_data:
            raise Exception("Make sure the coordinates are in Germany or increase the distance.")

        formatted_data = self.format_data(json_data)
            
        return formatted_data