from django import forms
import datetime
from django.forms import ModelForm
from .models import Event, Question, Choice, TextResponse
from django.forms import MultiWidget
from django.forms.widgets import SelectDateWidget
from django.forms import EmailField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_time', 'plus_one_permissible']

class Questionform(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'isVisible']
                
class Choiceform(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text','id']


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class inviteNewUserform(forms.Form):
    username = forms.CharField(label='Invitee username', max_length=100)
                
class newChoiceform(forms.Form):
    choice_text = forms.CharField(label='new choice',max_length=100)
    
class TextResponseform(ModelForm):
    class Meta:
        model = TextResponse
        fields = ['answer']

