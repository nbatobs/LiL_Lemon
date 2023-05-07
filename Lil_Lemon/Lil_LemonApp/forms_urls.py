from django.urls import path
from .views import CreateBookingView,HomeView,RegisterView,MenuView,MenuItemsView
urlpatterns = [
    path('create_booking/',CreateBookingView.as_view(), name='create-booking'),
    path('',HomeView.as_view(), name='home'),
    path('register/',RegisterView.as_view(), name='register'),
    path('menu/', MenuItemsView.as_view(), name='menu-list')
    ]