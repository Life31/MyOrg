from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm
from django.forms import Textarea, Select, DateInput

from .models import User_info, Vacation, Message
User = get_user_model()

class DateInput(DateInput):
    input_type = 'date'


# создадим собственный класс для формы регистрации
# сделаем его наследником предустановленного класса UserCreationForm
class CreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
            
    class Meta(UserCreationForm.Meta):
        # укажем модель, с которой связана создаваемая форма
        model = User
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('first_name', 'last_name', 'username', 'email')


class User_infoForm(ModelForm):
   
    class Meta():
        model = User_info
        fields = (
            'otd_number', 'phone_number', 'reqs_access', 'stor_access', 'corr_access',
            'conf_access', 'pass_access', 'user_access', 'vacs_access',
        )
        
        # exclude = ['user','position', 'boss']
        widgets = {
            'phone_number': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
        }
    
class VacationForm(ModelForm):
   
    class Meta():
        model = Vacation
        exclude = ['user', 'year']
        widgets = {
            'id': Textarea(attrs={"cols": 40, "rows": 1,}),
            'how_long': Textarea(attrs={"cols": 40, "rows": 1,}),
            'day_start': DateInput(),
            'day_end': DateInput(),
            'can_redact': Textarea(attrs={"readonly": True, "cols": 40, "rows": 1,}),
        }

class MessageForm(ModelForm):
    class Meta():
        model = Message
        exclude = ['user_one', 'user_two', 'witch_write', 'pub_date', 'readed']
        widgets = {
            'text': Textarea(attrs={"cols": 40, "rows": 1,}),
        }