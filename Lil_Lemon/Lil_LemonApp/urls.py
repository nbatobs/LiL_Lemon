from django.urls import path
from .views import BookingView,MenuView,MenuDetailView,BookingDetailView
urlpatterns = [
    path('menu/',MenuView.as_view(),name ='menu-list'),
    path('menu/<int:pk>/',MenuDetailView.as_view(), name='menu-detail'),
    path('bookings/',BookingView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/',BookingDetailView.as_view(), name='booking-detail'),
]


