from django.forms.models import ModelForm
from django.forms import Textarea, Select, DateInput
from .models import Task, Card, Bord, Note


class DateInput(DateInput):
    input_type = 'date'


class TaskForm(ModelForm):

    class Meta():
        model = Task
        fields = (
            'text',
            'state',
            'persent',
            'day_start',
            'day_end',
            'result',
            'file',
            'image',
            'master',
            'slave',
            'card',
            'same_id',
            'bord_link',
        )
        widgets = {
            'result': Textarea(attrs={"cols": 40, "rows": 1, }),
            #'slave': Select(attrs={"cols": 40, "rows": 1, }),
            'text': Textarea(attrs={"cols": 40, "rows": 2, }),
            'persent': Textarea(attrs={"cols": 40, "rows": 1, }),
            'same_id': Textarea(
                attrs={"readonly": True, "cols": 40, "rows": 1, }
            ),
            'day_start': DateInput(),
            'day_end': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        '''Функция изменяет обьект из поля.
        Выпадающий список получает полные имена пользователей.
        Николай Емельянов вместо nikolay.emelyanov.'''

        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['master'].label_from_instance = (
            # lambda obj: "%s (%s)" % (obj.get_full_name(), obj.username)
            lambda obj: "%s" % obj.get_full_name()
        )
        self.fields['slave'].label_from_instance = (
            # lambda obj: "%s (%s)" % (obj.get_full_name(), obj.username)
            lambda obj: "%s" % obj.get_full_name()
        )
        self.fields['bord_link'].label_from_instance = (
            # lambda obj: "%s (%s)" % (obj.get_full_name(), obj.username)
            lambda obj: "%s" % obj.name
        )


class CardForm(ModelForm):

    class Meta():
        model = Card
        fields = (
            'name',
        )
        widgets = {
            'name': Textarea(attrs={"cols": 40, "rows": 1, }),
        }


class BordForm(ModelForm):

    class Meta():
        model = Bord
        fields = (
            'name',
        )
        widgets = {
            'name': Textarea(attrs={"cols": 40, "rows": 1, }),
        }

class NoteForm(ModelForm):

    class Meta():
        model = Note
        fields = (
            'text', 'same_id',
        )
        widgets = {
            'text': Textarea(attrs={"cols": 80, "rows": 16, }),
            'same_id': Textarea(
                attrs={"readonly": True, "cols": 40, "rows": 1, }
            ),
        }
