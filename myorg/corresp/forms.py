from django.forms.models import ModelForm
from django.forms import Textarea, Select, DateInput

from .models import Corresp

class DateInput(DateInput):
    input_type = 'date'

class CorrespForm(ModelForm):

    class Meta():
        model = Corresp
        fields = ('number', 'in_out', 'company', 'from_who', 'to', 'day', 'comment', 'file', 'tag')

        widgets = {
            'number': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
            'company': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
            'day': DateInput(),
            'comment': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
            'tag': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
        }
