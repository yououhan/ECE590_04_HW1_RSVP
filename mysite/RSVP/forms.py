from django import forms
import datetime
from django.forms import ModelForm
from .models import Event, Question, Choice
from django.forms import MultiWidget
from django.forms.widgets import SelectDateWidget
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_time']
#        widgets = {'event_time' : forms.SelectDateWidget()}

class Questionform(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'isEditable', 'isOptional']
                
class Choiceform(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
