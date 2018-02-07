from django import forms
import datetime
from django.forms import ModelForm
from .models import Event, Question, Choice
from django.forms import MultiWidget
from django.forms.widgets import SelectDateWidget
from django.forms import EmailField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_time']
#        widgets = {'event_time' : forms.SelectDateWidget()}

class Questionform(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'isEditable', 'isOptional']
        widgets = {'question_text' : forms.TextInput(attrs={'placeholder': '11111'})}
                
class Choiceform(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']


class UserCreationForm(UserCreationForm):
#    email = EmailField(label=_("Email address"), required=True,
#                       help_text=_("Required."))
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    # def save(self, commit=True):
    #     user = super(UserCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user

class inviteNewform(forms.Form):
    new_userName = forms.CharField(label='New userName', max_length=100)
        
