from django.shortcuts import render
from .serializer import MenuSerializer,BookingSerializer,CustomTokenObtainPairSerializer
from rest_framework import generics
from .models import Menu,Booking
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.views import View
from django.http import HttpResponseForbidden
from rest_framework.permissions import BasePermission
from datetime import datetime,timedelta
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import BookingForm,MenuForm,RegisterForm
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import Group
from django.contrib import messages
from django.views.generic.edit import FormView



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        self.set_jwt_cookie(response)
        return response

    def set_jwt_cookie(self, response):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = RefreshToken(serializer.validated_data['refresh'])
        access_token = str(refresh_token.access_token)

        # Set token expiration time
        lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        expires = timezone.now() + lifetime

        # Create cookie with token data
        cookie_data = {
            'access_token': access_token,
            'refresh_token': str(refresh_token),
            'expires': expires.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'domain': settings.SESSION_COOKIE_DOMAIN,
            'secure': settings.SESSION_COOKIE_SECURE or None,
            'httponly': True,
            'samesite': 'None',
        }

        # Set the cookie on the response
        response.set_cookie(
            key='jwt',
            value=cookie_data['access_token'],
            expires=cookie_data['expires'],
            domain=cookie_data['domain'],
            secure=cookie_data['secure'],
            httponly=cookie_data['httponly'],
            samesite=cookie_data['samesite']
        )

#class MyTokenRefreshView(TokenRefreshView):
#    serializer_class = MyTokenObtainPairSerializer


class MenuView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Staff').exists()

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsStaff]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class BookingView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class CreateBookingView(View):
    form_class = BookingForm
    template_name = 'create_booking.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking-list')
        return render(request, self.template_name, {'form': form})

class HomeView(TemplateView):
    template_name = 'home.html'

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        group = Group.objects.get(name='Customers')
        user = form.save()
        user.groups.add(group)
        return response

class MenuItemsView(View):
    def get(self, request):
        menu_items = Menu.objects.all()
        return render(request, 'menu.html', {'menu_items': menu_items})