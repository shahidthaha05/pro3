from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['g_id','title', 'description', 'release_date', 'price', 'image']



from .models import Slot

# class SlotForm(forms.ModelForm):
#     class Meta:
#         model = Slot
#         fields = ['game', 'start_time', 'end_time', 'reserved']




# from django import forms
# from .models import Slot


# class SlotBookingForm(forms.Form):
#     slots = forms.ModelMultipleChoiceField(
#         queryset=Slot.objects.filter(reserved=False),
#         widget=forms.CheckboxSelectMultiple,
#         required=True,
#     )


from django import forms
from .models import Slot

class SlotBookingForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['time_slot']

    def __init__(self, *args, **kwargs):
        super(SlotBookingForm, self).__init__(*args, **kwargs)
        
        # Show only slots that are NOT reserved
        self.fields['time_slot'].widget = forms.Select(
            choices=[(slot, slot) for slot in Slot.TIME_SLOT_CHOICES if not Slot.objects.filter(time_slot=slot[0], reserved=True).exists()]
        )





