
# Register your models here.


from django.contrib import admin
from .models import Game, Slot

class SlotAdmin(admin.ModelAdmin):
    list_display = ('game', 'start_time', 'end_time', 'reserved')
    list_filter = ('game', 'reserved')
    search_fields = ('game__title', 'start_time', 'end_time')

admin.site.register(Game)
admin.site.register(Slot, SlotAdmin)
