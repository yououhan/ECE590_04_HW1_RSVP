from django.shortcuts import get_object_or_404, render
from .models import Event,People

#testing
def sign_in(request):
    Events = Event.objects.all()
    
    return render(request, 'RSVP/sign_in.html', {
        # don't forget to pass it in, and the last comma
        'Events': Events,
    })

# Create your views here.
#def sign_in(request):
    # View code here...
#    return render(request, 'RSVP/sign_in.html')

def home(request,people_id):
    people = get_object_or_404(People,pk = people_id)
    return render(request,'RSVP/home.html',{
        'username' : people.username,
        
    })
    # View code here...
#n    return render(request, 'RSVP/home.html')

def events_list(request, event_id):
    event = get_object_or_404(Event, pk = event_id)
    return render(request, 'RSVP/events_list.html', {
        'event_name': event.event_name,
        'event_time': event.event_time
    })
#pass the event ID here and can use the get object funciton

def index(request):
    from django import forms
    class NameForm(forms.Form):
        your_name = forms.CharField(label='Your name', max_length=100)
    template = "RSVP/index.html"
    context = { "form" : NameForm() }
    return render( request, template, context )
#    return render(request, 'RSVP/startbootstrap-landing-page/index.html')
#    return render(request, 'RSVP/index.html')
def sign_up(request):
    from django import forms
    class NameForm(forms.Form):
        your_name = forms.CharField(label='Your name', max_length=100)
    template = "RSVP/sign_up.html"
    context = { "form" : NameForm() }
    return render( request, template, context )
