import time
import requests

from django.core.management.base import BaseCommand

from fuel_optimizer_app.models import FuelStation


class Command(BaseCommand):

    help = "Geocode stations"


    def handle(self, *args, **kwargs):

        stations = FuelStation.objects.filter(
            latitude__isnull=True
        )

        for station in stations:

            query = (
                f"{station.address}, "
                f"{station.city}, "
                f"{station.state}, USA"
            )

            url = "https://nominatim.openstreetmap.org/search"

            params = {
                "q": query,
                "format": "json",
                "limit": 1,
            }

            headers = {
                "User-Agent": "fuel-optimizer"
            }

            response = requests.get(
                url,
                params=params,
                headers=headers,
            )

            data = response.json()

            if data:

                station.latitude = float(data[0]["lat"])
                station.longitude = float(data[0]["lon"])

                station.save()

                print(
                    f"✓ {station.name}"
                )

            else:

                print(
                    f"✗ Not found: {query}"
                )

            time.sleep(1)