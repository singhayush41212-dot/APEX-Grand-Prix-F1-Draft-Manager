import json
from pathlib import Path
from src.models import Driver, Principal, Car

def load_data():
    json_path = Path("drivers.json")
    if not json_path.exists():
        json_path = Path("../drivers.json")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    drivers = [
        Driver(name=d["name"], team=d["team"], year=d["year"], ovr=d["ovr"])
        for d in data["drivers"]
    ]

    principals = [
        Principal(name=p["name"], ovr=p["ovr"], year=p["year"], special=p["special"])
        for p in data["principals"]
    ]

    cars = [
        Car(name=c["name"], team=c["team"], year=c["year"], ovr=c["ovr"])
        for c in data.get("cars", [])
    ]

    return drivers, principals, cars