from cgitb import enable
from csv import field_size_limit
from django.forms.models import ModelForm
from django.forms import Textarea, Select, DateInput

from .models import Unswers, Question

class DateInput(DateInput):
    input_type = 'date'


class UnswersForm(ModelForm):
   
    class Meta():
        model = Unswers
        exclude = ['user', 'test']

        widgets = {
            'unswer_1': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_2': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_3': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_4': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_5': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_6': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_7': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_8': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_9': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_10': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_11': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_12': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_13': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_14': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_15': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_16': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_17': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_18': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_19': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
            'unswer_20': Textarea(attrs={'readonly': True, "cols": 40, "rows": 1,}),
        }

class QuestionForm(ModelForm):

    class Meta():
        model = Question
        exclude = []
        widgets = {
            
            'quest': Textarea(attrs={"cols": 20, "rows": 1,}),
            'right_unswer': Textarea(attrs={"cols": 20, "rows": 1,}),
            'unswer_2': Textarea(attrs={"cols": 20, "rows": 1,}),
            'unswer_3': Textarea(attrs={"cols": 20, "rows": 1,}),
            'unswer_4': Textarea(attrs={"cols": 20, "rows": 1,}),
            'test': Textarea(attrs={"cols": 20, "rows": 1,}),
            'same_id': Textarea(attrs={"cols": 20, "rows": 1,}),
         }