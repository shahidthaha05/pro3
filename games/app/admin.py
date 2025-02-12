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


from django.contrib import admin
from .models import Game, Slot

class SlotAdmin(admin.ModelAdmin):
    list_display = ('time_slot', 'reserved')  # Display slots globally
    list_filter = ('reserved',)  # Filter by reservation status
    search_fields = ('time_slot',)  # Allow searching by time slot

admin.site.register(Game)
admin.site.register(Slot, SlotAdmin)



# Register your models with their corresponding admin configurations
