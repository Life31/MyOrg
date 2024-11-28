from django.forms.models import ModelForm
from django.forms import Textarea, Select, DateInput

from .models import Unit, Include, Config, Query, Change, Configuration, Changes, Changes_confirm

class DateInput(DateInput):
    input_type = 'date'


class UnitForm(ModelForm):
   
    class Meta():
        model = Unit
        fields = ('unit_type', 'position', 'creator', 'serial_n',
                  'part_n', 'descr', 'doc', )

        widgets = {
                'unit_type': Textarea(attrs={"cols": 40, "rows": 1,}),
                'position': Textarea(attrs={"cols": 40, "rows": 1}),
                'creator': Textarea(attrs={"cols": 40, "rows": 1}),
                'serial_n': Textarea(attrs={"cols": 40, "rows": 1}),
                'part_n': Textarea(attrs={"cols": 40, "rows": 1}),
                'descr': Textarea(attrs={"cols": 40, "rows": 1}),
                }

class IncludeForm(ModelForm):
    
    class Meta:
        model = Include
        fields = ('name', )
        widgets = {'name': Textarea(attrs={"cols": 40, "rows": 1}),
                   }


class ConfigForm(ModelForm):
   
    class Meta():
        model = Config
        fields = ('unit', 'include_name', 'part_n',
                  'other_info', 'descr', 'doc', )

        widgets = {
                'part_n': Textarea(attrs={"cols": 40, "rows": 1,}),
                'other_info': Textarea(attrs={"cols": 40, "rows": 1}),
                'descr': Textarea(attrs={"cols": 40, "rows": 1}),
                }


class ChangeForm(ModelForm):
   
    class Meta():
        model = Change
        fields = ('number', 'unit', 'include_name', 'part_n',
                  'other_info', 'descr', 'doc', 'state', )

        widgets = {
                'part_n': Textarea(attrs={"cols": 40, "rows": 1,}),
                'other_info': Textarea(attrs={"cols": 40, "rows": 1}),
                'descr': Textarea(attrs={"cols": 40, "rows": 1}),
                'state': Textarea(attrs={"cols": 40, "rows": 1}),
                }

#---------------------------------------------------------new
class ConfigurationForm(ModelForm):
   
    class Meta():
        model = Configuration
        fields = ('parametr', 'part_n',
                  'other_info', 'descr', 'doc', )

        widgets = {
                #'unit': Select(attrs={'disabled': True, "cols": 40, "rows": 1,}),
                'parametr': Textarea(attrs={"cols": 40, "rows": 1,}),
                'part_n': Textarea(attrs={"cols": 40, "rows": 1,}),
                'other_info': Textarea(attrs={"cols": 40, "rows": 1}),
                'descr': Textarea(attrs={"cols": 40, "rows": 1}),
                }

class Changes_confirmForm(ModelForm):
   
    class Meta():
        model = Changes_confirm
        fields = ('parametr', 'part_n',
                  'other_info', 'descr', 'doc', )

        widgets = {
                #'unit': Select(attrs={'disabled': True, "cols": 40, "rows": 1,}),
                'parametr': Textarea(attrs={"cols": 40, "rows": 1,}),
                'part_n': Textarea(attrs={"cols": 40, "rows": 1,}),
                'other_info': Textarea(attrs={"cols": 40, "rows": 1}),
                'descr': Textarea(attrs={"cols": 40, "rows": 1}),
                }

#---------------------------------------------------------new