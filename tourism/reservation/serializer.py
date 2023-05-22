"""serializer for reservation"""

from rest_framework import serializers

from core.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'title', 'type', 'created_at', 'updated_at']
        read_only_fields = ['id']


class ReservationDetailSerializer(ReservationSerializer):
    """Serializer for reservations detail views"""
    class Meta(ReservationSerializer.Meta):
        fields = ReservationSerializer.Meta.fields + ['detail']
