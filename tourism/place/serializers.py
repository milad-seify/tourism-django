from rest_framework_gis import serializers

from .models import (
    Places,
    TourismPlace,
    ShoppingPlace,
    RecreationalPlace)


class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        fields = '__all__'
        read_only_field = 'id'


class TourismSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = TourismPlace
        fields = ('id', 'image', 'place_id')
        geo_field = 'location'
        read_only_field = 'id'


class ShoppingSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = ShoppingPlace
        fields = ('id', 'image', 'place_id')
        geo_field = 'location'
        read_only_field = 'id'


class RecreationalSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = RecreationalPlace
        fields = ('id', 'image', 'place_id')
        geo_field = 'location'
        read_only_field = 'id'
