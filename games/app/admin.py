from django.contrib import admin
from .models import Game, Slot

class SlotInline(admin.TabularInline):
    model = Slot
    extra = 1  # The number of empty slots to display by default (you can adjust this)
    fields = ['start_time', 'end_time', 'reserved']  # Fields to display in the inline form
    readonly_fields = ['reserved']  # Make 'reserved' read-only so it can't be manually edited in the inline form

class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'price')  # Customize columns to display for the Game model
    search_fields = ('title',)  # Allow searching by the game's title
    inlines = [SlotInline]  # Display Slot as inline within the Game model

class SlotAdmin(admin.ModelAdmin):
    list_display = ('game', 'start_time', 'end_time', 'reserved')  # Customize columns to display for the Slot model
    list_filter = ('game', 'reserved')  # Allow filtering slots by game and reserved status
    search_fields = ('game__title', 'start_time', 'end_time')  # Allow searching by game title or slot times

# Register your models with their corresponding admin configurations
admin.site.register(Game, GameAdmin)
admin.site.register(Slot, SlotAdmin)
