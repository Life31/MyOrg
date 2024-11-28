from django.forms.models import ModelForm
from django.forms import Textarea, Select, DateInput

from .models import Unit, Th, Creator, Ctgry, Place, Si, Stend, Tag, Th_tags, Event

class DateInput(DateInput):
    input_type = 'date'

class UnitForm(ModelForm):

    class Meta():
        model = Unit
        fields = ('name', 'code', 'creator', 
                  'ctgry', 'place', 'si',
                  'num', 'box', 'stend', 'comment', 'image', 'acctual',)
        widgets = {'name': Textarea(attrs={"cols": 40, "rows": 1}),
                   'creator': Select(attrs={"cols": 40, "rows": 1}),
                   'code': Textarea(attrs={"cols": 40, "rows": 1}),
                   'ctgry': Select(attrs={"cols": 40, "rows": 1}),
                   'place': Select(attrs={"cols": 40, "rows": 1}),
                   'si': Select(attrs={"cols": 40, "rows": 1}),
                   'num': Textarea(attrs={"cols": 40, "rows": 1}),
                   'box': Textarea(attrs={"cols": 40, "rows": 1}),
                   'stend': Select(attrs={"cols": 40, "rows": 1}),
                   'comment': Textarea(attrs={"cols": 40, "rows": 1})}


class ThForm(ModelForm):

    class Meta():
        model = Th
        fields = ('title', 'year', 'type_th',
                  'th', 'day', 'comment', 'unit_number')
        widgets = {
            'title': Textarea(attrs={"cols": 40, "rows": 1}),
            'year': Select(attrs={"cols": 40, "rows": 1}),
            'type_th': Select(attrs={"cols": 40, "rows": 1}),
            'day': DateInput(),
            'comment': Textarea(attrs={"cols": 40, "rows": 1}),
            'unit_number': Textarea(attrs={"cols": 40, "rows": 1}),
        }



class CreatorForm(ModelForm):

    class Meta():
        model = Creator
        fields = ('title', 'description')
        widgets = {'title': Textarea(attrs={"cols": 40, "rows": 1}),
                   'description': Textarea(attrs={"cols": 40, "rows": 2})}


class CtgryForm(ModelForm):

    class Meta():
        model = Ctgry
        fields = ('title', 'description')
        widgets = {'title': Textarea(attrs={"cols": 40, "rows": 1}),
                   'description': Textarea(attrs={"cols": 40, "rows": 2})}


class PlaceForm(ModelForm):

    class Meta():
        model = Place
        fields = ('title', 'description')
        widgets = {'title': Textarea(attrs={"cols": 40, "rows": 1}),
                   'description': Textarea(attrs={"cols": 40, "rows": 2})}


class SiForm(ModelForm):

    class Meta():
        model = Si
        fields = ('title', 'description')
        widgets = {'title': Textarea(attrs={"cols": 40, "rows": 1}),
                   'description': Textarea(attrs={"cols": 40, "rows": 2})}


class StendForm(ModelForm):

    class Meta():
        model = Stend
        fields = ('title', 'description')
        widgets = {'title': Textarea(attrs={"cols": 40, "rows": 1}),
                   'description': Textarea(attrs={"cols": 40, "rows": 2})}


class TagForm(ModelForm):

    class Meta():
        model = Tag
        fields = ('tag',)
        widgets = {'title': Textarea(attrs={"cols": 40, "rows": 1}),}


class Tag_addForm(ModelForm):

    class Meta():
        model = Th_tags
        fields = ('tag',)
        widgets = {'tag': Select(attrs={"cols": 40, "rows": 1}),
                   } 

class EventForm(ModelForm):

    class Meta():
        model = Event
        fields = ('th_name', 'unit_name', 'event_name', 
                  'num', 'date', 'comment',)
        widgets = {'th_name': Select(attrs={"cols": 40, "rows": 1}),
                   'unit_name': Select(attrs={'disabled': True, "cols": 40, "rows": 1}),
                   'event_name': Select(attrs={"cols": 40, "rows": 1}),
                   'num': Textarea(attrs={"cols": 40, "rows": 1}),
                   'date': DateInput(),
                   'comment': Textarea(attrs={"cols": 40, "rows": 1}),}
