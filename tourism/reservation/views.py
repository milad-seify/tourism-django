"""Views for Reservation APIs"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Reservation
from reservation.serializer import (
    ReservationSerializer, ReservationDetailSerializer)


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
