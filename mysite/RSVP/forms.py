from django import forms
import datetime

class EventForm(forms.Form):
    event_name = forms.CharField(label='Event name', max_length=100)
    event_time = forms.DateTimeField()
