from django.forms.models import ModelForm
from django.forms import Textarea, Select, DateInput

from .models import Pass, Car_pass

class DateInput(DateInput):
    input_type = 'date'

class PassForm(ModelForm):
   
    class Meta():
        model = Pass
        fields = ('num', 'sec_name', 'name', 'patro', 'where', 'day', 'doc_type', 'pasport', 'spec', 'comment')

        widgets = {
                'num': Textarea(attrs={"readonly": True, "cols": 40, "rows": 1,}),
                'name': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'sec_name': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'patro': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'where': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'day': DateInput(),
                'doc_type': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'pasport': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'spec': Select(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'comment': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),                
                  }


class Car_passForm(ModelForm):
   
    class Meta():
        model = Car_pass
        fields = ('num', 'phone', 'name', 'sec_name', 'patro', 'pasport', 'trans', 
                'auto', 'num_auto', 'stuff', 'quantity', 'day', 'comment')

        widgets = {
                'num': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'phone': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'name': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'sec_name': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'patro': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'pasport': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'trans': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'auto': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'stuff': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'quantity': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),            
                'day': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'comment': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                  }


class PassForm_Admin(ModelForm):
   
    class Meta():
        model = Pass
        fields = ('num', 'name', 'sec_name', 'patro', 'where', 'day', 'comment',
                  'author')

        widgets = {
                'num': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'name': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'sec_name': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'patro': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'where': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'day': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'comment': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
                'author': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),                
                  }
