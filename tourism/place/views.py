

# from rest_framework.generics import ListAPIView
from rest_framework import viewsets
# from rest_framework_gis import filters
from .serializers import (
    PlacesSerializer,
    RecreationalSerializer,
    TourismSerializer,
    ShoppingSerializer,
)
from .models import (
    Places,
    RecreationalPlace,
    TourismPlace,
    ShoppingPlace
)


class PlacesApiView(viewsets.ReadOnlyModelViewSet):
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer


class ShoppingApiView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ShoppingSerializer
    queryset = ShoppingPlace.objects.all()
    # bbox_filter_field = 'location'
    # filter_backends = (filters.InBBOXFilter,)


class TourismApiView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TourismSerializer
    queryset = TourismPlace.objects.all()
    # bbox_filter_field = 'location'
    # filter_backends = (filters.InBBOXFilter,)


class RecreationalApiView(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecreationalSerializer
    queryset = RecreationalPlace.objects.all()
    # bbox_filter_field = 'location'
    # filter_backends = (filters.InBBOXFilter,)
