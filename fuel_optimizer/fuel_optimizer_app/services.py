import requests
import polyline
from math import radians, sin, cos, sqrt, atan2
from .models import FuelStation

from fuel_optimizer_app.models import FuelStation
from django.conf import settings

import requests

from fuel_optimizer_app.models import FuelStation
def get_route(start_coords, finish_coords):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": settings.ORS_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "coordinates": [
            start_coords,
            finish_coords
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=20
    )
    print("STATUS:", response.status_code)
    # print("RESPONSE:", response.text)

    response.raise_for_status()

    data = response.json()

    feature = data["routes"][0]

    geometry = feature["geometry"]

    distance_miles = feature["summary"]["distance"] * 0.000621371

    duration_hours = feature["summary"]["duration"] / 3600

    route_points = polyline.decode(geometry)

    return {
        "distance_miles": distance_miles,
        "duration_hours": duration_hours,
        "polyline": geometry,
        "route_points": route_points,
    }
    


def haversine(lat1, lon1, lat2, lon2):
    R = 3959

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    return 2 * R * atan2(sqrt(a), sqrt(1 - a))



def get_candidate_stations(route_points):
    """
    Find stations within 10 miles of the route.
    Uses only stations that already have coordinates.
    """

    candidates = []

    # Only consider stations that have been geocoded
    stations = FuelStation.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False,
    )

    # Reduce route points to improve performance
    sampled_route = route_points[::25]

    for station in stations:

        for lat, lon in sampled_route:

            dist = haversine(
                station.latitude,
                station.longitude,
                lat,
                lon,
            )

            if dist <= 10:
                candidates.append(station)
                break

    return candidates
def optimize_fuel(stations, total_distance):
    mpg = 10
    max_range = 500

    # No stations found near route
    if not stations:
        return []

    fuel_stops = []
    remaining = total_distance

    while remaining > 0:
        segment = min(max_range, remaining)

        gallons = segment / mpg

        station = min(
            stations,
            key=lambda x: x.retail_price
        )

        cost = gallons * station.retail_price

        fuel_stops.append({
            "name": station.name,
            "city": station.city,
            "state": station.state,
            "price": round(station.retail_price, 2),
            "gallons": round(gallons, 2),
            "cost": round(cost, 2),
        })

        remaining -= segment

    return fuel_stops

def geocode_station(station):
    """
    Geocode a station only if coordinates are missing.
    """

    if station.latitude and station.longitude:
        return station

    query = (
        f"{station.address}, "
        f"{station.city}, "
        f"{station.state}, USA"
    )

    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={
            "q": query,
            "format": "json",
            "limit": 1,
        },
        headers={
            "User-Agent": "fuel-optimizer"
        },
        timeout=20,
    )

    data = response.json()

    if not data:
        return None

    station.latitude = float(data[0]["lat"])
    station.longitude = float(data[0]["lon"])

    station.save(
        update_fields=["latitude", "longitude"]
    )

    return station