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




from django import forms
from .models import Slot


class SlotBookingForm(forms.Form):
    slots = forms.ModelMultipleChoiceField(
        queryset=Slot.objects.filter(reserved=False),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )





class UserDetailsForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15, required=False)
