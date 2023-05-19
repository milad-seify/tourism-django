"""Serializers for the user API view"""

from django.contrib.auth import (get_user_model, authenticate,)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user objects."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name',
                  'address', 'phone_number', 'card_info']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5},
                        'phone_number': {'write_only': True, 'min_length': 11}, }

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().\
            objects.create_user(**validated_data)  # type: ignore

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        card_info = validated_data.pop('card_info', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        if card_info:
            user.set_card_info(card_info)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        required=True,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
