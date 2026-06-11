import pandas as pd

from django.core.management.base import BaseCommand

from fuel_optimizer_app.models import FuelStation


class Command(BaseCommand):
    help = "Import fuel stations"


    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)


    def handle(self, *args, **options):

        csv_path = options["csv_path"]

        df = pd.read_csv(csv_path)

        df = df.drop_duplicates()

        stations = []

        for _, row in df.iterrows():

            stations.append(
                FuelStation(
                    truckstop_id=row.get("OPIS Truckstop ID"),
                    name=row["Truckstop Name"],
                    address=row["Address"],
                    city=row["City"],
                    state=row["State"],
                    retail_price=row["Retail Price"],
                )
            )

        FuelStation.objects.bulk_create(
            stations,
            batch_size=1000
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(stations)} stations"
            )
        )