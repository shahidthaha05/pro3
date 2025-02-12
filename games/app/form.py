from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['g_id','title', 'description', 'release_date', 'price', 'image']


from django import forms
from .models import Slot

class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['game', 'start_time', 'end_time', 'reserved']
