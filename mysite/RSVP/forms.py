from django import forms
import datetime

class EventForm(forms.Form):
    event_name = forms.CharField(label='Event name', max_length=100)
    event_time = forms.DateTimeField()


class QuestionForm(forms.Form):
    question_text = forms.CharField(label='Question',max_length=200)
    question_type = forms.CharField(label='type', max_length = 1)
#    isEditable = forms.BooleanField(label='editable')
#    isOptional = forms.BooleanField(label='optional')
    
    
