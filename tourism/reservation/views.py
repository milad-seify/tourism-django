"""Views for Reservation APIs"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import filters
from core.models import (Reservation, HotelAndResidence,
                         TravelAgency, TouristTour)
from reservation.serializer import (
    ReservationDetailSerializer,
    TravelAgencySerializer,
    ReservationSerializer,
    HotelAndResidenceSerializer,
    TouristTourSerializer
)


class ReservationView(viewsets.ModelViewSet):
    """View for manage reservation APIs"""
    serializer_class = ReservationDetailSerializer
    queryset = Reservation.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve reservations for authenticated user."""
        return self.queryset.filter(user=self.request.user)\
            .order_by('-created_at')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return ReservationSerializer

        return self.serializer_class

    def perform_create(self, serializers):
        """Create a new reservation with correct user"""
        serializers.save(user=self.request.user)


class HotelAndResidenceView(viewsets.ModelViewSet):
    serializer_class = HotelAndResidenceSerializer
    queryset = HotelAndResidence.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['name']
    filter_backends = [filters.SearchFilter]
    search_fields = ['$name']

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(reservation__user=user)


class TourismTourView(viewsets.ModelViewSet):
    serializer_class = TouristTourSerializer
    queryset = TouristTour.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(reservation__user=user)


class TravelAgencyView(viewsets.ModelViewSet):
    serializer_class = TravelAgencySerializer
    queryset = TravelAgency.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(reservation__user=user)
