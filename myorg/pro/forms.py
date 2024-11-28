from django.forms.models import ModelForm
from django.forms import Textarea, Select, DateInput

from .models import Block, Event

class DateInput(DateInput):
    input_type = 'date'

class BlockForm(ModelForm):
   
    class Meta():
        model = Block
        fields = ('block_type', 'number', 'info', 'block_state', 'on_ready', 'day')

        widgets = {
            'number': Textarea(attrs={"cols": 40, "rows": 1,}),
            'info': Textarea(attrs={"cols": 40, "rows": 1,}),
            'day': DateInput(),               
        }

class EventForm(ModelForm):
   
    class Meta():
        model = Event
        fields = ('block', 'event_type', 'description', 'day', )

        widgets = {
            'event_type': Select(attrs={"cols": 40, "rows": 1,}),
            'description': Textarea(attrs={"cols": 40, "rows": 1,}),
            'day': DateInput(),               
        }
