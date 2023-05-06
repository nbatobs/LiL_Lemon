from rest_framework import serializers
from .models import Booking,Menu
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta,datetime
from django.conf import settings



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Set token expiration time
        token.set_exp(lifetime=timedelta(minutes=5))

        # Return the token
        return token

    def get_cookie_data(self):
        token = self.validated_data.get('access')
        if token is None:
            return {}
        token_str = str(token)
        cookie_data = {
            'access_token': token_str,
            'refresh_token': str(self.validated_data.get('refresh')),
            'expires': (datetime.utcnow() + timedelta(minutes=5)).strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'domain': settings.SESSION_COOKIE_DOMAIN,
            'secure': settings.SESSION_COOKIE_SECURE or None,
            'httponly': True,
            'samesite': 'None',
        }
        return cookie_data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['id','name', 'no_of_guests', 'date']


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ['id','title', 'price', 'inventory']

