from django.contrib import admin
from.models import Booking,Menu

class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'no_of_guests', 'date')
    list_filter = ('date',)
    search_fields = ('name',)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'inventory')
    list_filter = ('inventory',)
    search_fields = ('title',)

admin.site.register(Booking, BookingAdmin)
admin.site.register(Menu, MenuAdmin)