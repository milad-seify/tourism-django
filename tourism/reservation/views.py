"""Views for Reservation APIs"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Reservation
from reservation.serializer import ReservationSerializer


class ReservationView(viewsets.ModelViewSet):
    """View for manage reservation APIs"""
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve reservations for authenticated user."""
        return self.queryset.filter(user=self.request.user)\
            .order_by('-created_at')
