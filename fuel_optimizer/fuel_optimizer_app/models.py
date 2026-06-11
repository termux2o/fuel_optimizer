from django.db import models


class FuelStation(models.Model):
    truckstop_id = models.IntegerField(null=True, blank=True)

    name = models.CharField(max_length=255)

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=10)

    address = models.CharField(max_length=255, blank=True)

    latitude = models.FloatField(null=True, blank=True)

    longitude = models.FloatField(null=True, blank=True)

    retail_price = models.FloatField()