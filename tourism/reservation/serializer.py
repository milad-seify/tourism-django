"""serializer for reservation"""

from django.contrib.auth import (get_user_model, authenticate,)

from rest_framework import serializers
from user.serializers import UserSerializer
from rest_framework.exceptions import ValidationError

from core.models import (
    Reservation,
    HotelAndResidence,
    TravelAgency,
    TouristTour,
)


class ReservationSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Reservation
        fields = ['id', 'title', 'type', 'created_at',
                  'updated_at']
        # fields = '__all__'
        read_only_fields = ['id']


class HotelAndResidenceSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(
        required=False, allow_null=True)
    # reservation = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = HotelAndResidence
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'address': {'required': False},
            'facilities': {'required': False},
            'cost': {'required': False},
        }

    def create(self, validated_data):
        user = self.context['request'].user  # type: ignore
        user_id = user.id  # type: ignore
        has_reservation = Reservation.objects.filter(user=user).exists()
        reservation_data = validated_data.pop('reservation', None)

        if has_reservation:
            reservation = Reservation.objects.filter(user=user.id).first()
            reservation.type = 'HOTEL_AND_RESIDENCE'  # type: ignore
            reservation.save()  # type: ignore

        elif reservation_data is not None and reservation_data.get('user') and reservation_data['user']['id'] == user_id:
            reservation = reservation_data.get('id')

        else:
            reservation = Reservation.objects.create(
                user=user,
                title=user.first_name,
                type='HOTEL_AND_RESIDENCE'
            )

        hotel = HotelAndResidence.objects.create(
            reservation=reservation, **validated_data)

        return hotel


class TouristTourSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(
        required=False, allow_null=True)

    class Meta:
        model = TouristTour
        fields = '__all__'
        read_only_field = ['id']
        extra_kwargs = {
            'facilities': {'required': False},
            'cost': {'required': False},
        }

    def create(self, validated_data):
        user = self.context['request'].user  # type: ignore
        user_id = user.id  # type: ignore
        has_reservation = Reservation.objects.filter(user=user).exists()
        reservation_data = validated_data.pop('reservation', None)

        if has_reservation:
            reservation = Reservation.objects.filter(user=user.id).first()
            reservation.type = 'TOURIST_TOUR'  # type: ignore
            reservation.save()  # type: ignore

        elif reservation_data is not None and reservation_data.get('user') and reservation_data['user']['id'] == user_id:
            reservation = reservation_data.get('id')

        else:
            reservation = Reservation.objects.create(
                user=user,
                title=user.first_name,
                type='TOURIST_TOUR'
            )

        tour = TouristTour.objects.create(
            reservation=reservation, **validated_data)

        return tour


class TravelAgencySerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(
        required=False, allow_null=True)

    class Meta:
        model = TravelAgency
        fields = '__all__'
        read_only_field = ['id']
        extra_kwargs = {

            'cost': {'required': False},
        }

    def create(self, validated_data):
        user = self.context['request'].user  # type: ignore
        user_id = user.id  # type: ignore
        has_reservation = Reservation.objects.filter(user=user).exists()
        reservation_data = validated_data.pop('reservation', None)

        if has_reservation:
            reservation = Reservation.objects.filter(user=user.id).first()
            reservation.type = 'TRAVEL_AGENCY'  # type: ignore
            reservation.save()  # type: ignore

        elif reservation_data is not None and reservation_data.get('user') and reservation_data['user']['id'] == user_id:
            reservation = reservation_data.get('id')

        else:
            reservation = Reservation.objects.create(
                user=user,
                title=user.first_name,
                type='TRAVEL_AGENCY'
            )

        agency = TravelAgency.objects.create(
            reservation=reservation, **validated_data)

        return agency


class ReservationDetailSerializer(ReservationSerializer):
    """Serializer for reservations detail views"""
    hotels = HotelAndResidenceSerializer(
        read_only=True, many=True, source='hotelandresidence_set')
    tours = TouristTourSerializer(
        read_only=True, many=True, source='touristtour_set')
    travel = TravelAgencySerializer(
        read_only=True, many=True, source='travelagency_set')

    class Meta(ReservationSerializer.Meta):
        fields = ReservationSerializer.Meta.fields + \
            ['detail', 'hotels', 'tours', 'travel']


# class HotelAndResidenceAllSerializer(serializers.ModelSerializer):
#     """with out reservation and user just you can see all exist HOTEL"""
#     class Meta:
#         model = HotelAndResidence
#         fields = ['id', 'name', 'type_hotel', 'address',
#                   'facilities', 'star', 'cost']
#         read_only_fields = ['id']
