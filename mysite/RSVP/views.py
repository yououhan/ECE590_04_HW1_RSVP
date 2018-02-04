from django.shortcuts import get_object_or_404, render
from .models import Event,People,RegisterEvent

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
    own =  RegisterEvent.objects.filter(people=people,identity=0)
    ownEventsPending = own.filter(register_state = 0)
    ownEvents = own.filter(register_state = 1)
    # ownHistory = ownEvents.filter(event.event_time < timezone.now)
    guest = RegisterEvent.objects.filter(people=people,identity = 2)
    guestPending = guest.filter(register_state = 0)
    guestEvents = guest.filter(register_state = 1)
    vender = RegisterEvent.objects.filter(people=people,identity = 1)
    venderPending = vender.filter(register_state = 0)
    venderEvents = vender.filter(register_state = 1)
    return render(request,'RSVP/home.html',{
        'username' : people.username,
        'ownEventsPending': ownEventsPending,
        'ownEvents':ownEvents,
        'guestPending':guestPending,
        'guestEvents':guestEvents,
        'venderPending':venderPending,
        'venderEvents':venderEvents
    })
    # View code here...
#n    return render(request, 'RSVP/home.html')

def events_list(request, event_id):
    event = get_object_or_404(Event, pk = event_id)
    guest = RegisterEvent.objects.filter(event=event,identity=2)
    guestNum = guest.count()
 #   user = request.People
    return render(request, 'RSVP/events_list.html', {
        'event_name': event.event_name,
        'event_time': event.event_time,
        'guest':guest,
        'guestNum':guestNum
  #      'user':user
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
