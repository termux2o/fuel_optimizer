from rest_framework import serializers


class RouteSerializer(serializers.Serializer):
    start = serializers.CharField()
    finish = serializers.CharField()