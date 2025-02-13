from django.contrib import admin
from .models import Game, Slot, SlotBooking

class SlotInline(admin.TabularInline):
    model = Slot
    extra = 1  
    fields = ['time_slot']  # Removed 'booking_time' since it's not a field
    readonly_fields = []  # Removed 'booking_time' from readonly

class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'price')  
    search_fields = ('title',)  
    inlines = [SlotInline]  

class SlotAdmin(admin.ModelAdmin):
    list_display = ('time_slot', 'is_available')  
    list_filter = ('game',)  
    search_fields = ('time_slot',)  

    def is_available(self, obj):
        """Dynamically check if a slot is available based on booking time."""
        return obj.is_available()
    is_available.boolean = True  
    is_available.short_description = "Available"

class SlotBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'get_time_slot', 'date')  # Fixed 'time_slot' issue
    list_filter = ('game', 'date')

    def get_time_slot(self, obj):
        """Fetch the time slot from related Slot object"""
        return obj.slot.time_slot  # Make sure SlotBooking has a ForeignKey to Slot
    get_time_slot.short_description = "Time Slot"

admin.site.register(Game, GameAdmin)
admin.site.register(Slot, SlotAdmin)
admin.site.register(SlotBooking, SlotBookingAdmin)

