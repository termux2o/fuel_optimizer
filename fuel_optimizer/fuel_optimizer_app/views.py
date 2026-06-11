from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RouteSerializer
from .services import (
    get_route,
    get_candidate_stations,
    optimize_fuel,
)


class RouteAPIView(APIView):

    def post(self, request):

        serializer = RouteSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        start = serializer.validated_data["start"]
        finish = serializer.validated_data["finish"]

        cache_key = f"{start}:{finish}"

        cached = cache.get(cache_key)

        if cached:
            return Response(cached)

        start_coords = self.geocode(start)
        finish_coords = self.geocode(finish)

        route = get_route(start_coords, finish_coords)

        stations = get_candidate_stations(
            route["route_points"]
        )

        fuel_stops = optimize_fuel(
            stations,
            route["distance_miles"],
        )

        total = sum(x["cost"] for x in fuel_stops)

        result = {
            "distance_miles": round(route["distance_miles"], 2),
            "duration_hours": round(route["duration_hours"], 2),
            "fuel_stops": fuel_stops,
            "total_fuel_cost": round(total, 2),
            # "polyline": route["polyline"],
        }

        cache.set(cache_key, result, 86400)

        return Response(result)

    def geocode(self, location):
            import requests

            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "q": location,
                    "format": "json",
                    "limit": 1,
                },
                headers={
                    "User-Agent": "fuel-optimizer"
                },
                timeout=20,
            )

            response.raise_for_status()

            data = response.json()

            if not data:
                raise Exception(f"Could not geocode: {location}")

            return [
                float(data[0]["lon"]),   # IMPORTANT: longitude first
                float(data[0]["lat"]),   # latitude second
            ]