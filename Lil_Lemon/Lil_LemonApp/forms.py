from django import forms
from .models import Booking, Menu

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'no_of_guests', 'date']

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['title', 'price', 'inventory']
