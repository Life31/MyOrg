from django.forms.models import ModelForm
from django.forms import Textarea, Select, DateInput

from .models import Comment, Post, User, Feedback

class DateInput(DateInput):
    input_type = 'date'


class PostForm(ModelForm):
   
    class Meta():
        model = Post
        fields = ('text', 'unit', 'purpose',
                  'day', 't_start', 't_stop',
                  'reason', 'configuration', 'instruments',
                  'add_requirements', 'test_object', 'testers', 'doc',
                  'task_state', )

        widgets = {
                'text': Textarea(attrs={"readonly": True, "cols": 40, "rows": 1,}),
                'purpose': Textarea(attrs={"cols": 40, "rows": 1}),
                #'day': Textarea(attrs={"cols": 40, "rows": 1}),
                'day': DateInput(),
                #'time_start': Textarea(attrs={"cols": 40, "rows": 1}),
                #'time_stop': Textarea(attrs={"cols": 40, "rows": 1}),
                'configuration': Textarea(attrs={"cols": 40, "rows": 1}),
                'add_requirements': Textarea(attrs={"cols": 40, "rows": 1}),
                'reason': Textarea(attrs={"cols": 40, "rows": 1}),
                'instruments': Textarea(attrs={"cols": 40, "rows": 1}),
                'test_object': Textarea(attrs={"cols": 40, "rows": 1}),
                'testers': Textarea(attrs={"cols": 40, "rows": 1,}),
                'doc': Textarea(attrs={"cols": 40, "rows": 1,}),
                'task_state': Select(attrs={'disabled': True, "cols": 40, "rows": 1,}),
                }

class CommentForm(ModelForm):
    
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {'text': Textarea(attrs={"cols": 80, "rows": 1})}


class PostForm_nuc(ModelForm):
   
    class Meta():
        model = Post
        fields = ('unit', 'text', 'day', 't_start', 't_stop', )
        widgets = {
                'text': Textarea(attrs={"readonly": True,
                                        "cols": 40,
                                        "rows": 1,}),
                'day': DateInput(),
                }


class FeedbackForm(ModelForm):
    
    class Meta:
        model = Feedback
        fields = ('text', 'state', 'author', 'image')
        widgets = {'text': Textarea(attrs={"cols": 80, "rows": 2}),
                   'state': Select(attrs={'disabled': True, "cols": 40, "rows": 1,}),}
