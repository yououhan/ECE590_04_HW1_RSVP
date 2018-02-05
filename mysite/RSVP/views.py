from django.shortcuts import get_object_or_404, render,redirect
from .models import Event,RegisterEvent,Question
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import logout

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

def home(request):
    user = get_object_or_404(User,username = request.user.username)
    own =  RegisterEvent.objects.filter(user=user,identity=0)
    ownEventsPending = own.filter(register_state = 0)
    ownEvents = own.filter(register_state = 1)
    # ownHistory = ownEvents.filter(event.event_time < timezone.now)
    guest = RegisterEvent.objects.filter(user=user,identity = 2)
    guestPending = guest.filter(register_state = 0)
    guestEvents = guest.filter(register_state = 1)
    vendor = RegisterEvent.objects.filter(user=user,identity = 1)
    vendorPending = vendor.filter(register_state = 0)
    vendorEvents = vendor.filter(register_state = 1)
    return render(request,'RSVP/home.html',{
        'username' : user.username,
        'ownEventsPending': ownEventsPending,
        'ownEvents':ownEvents,
        'guestPending':guestPending,
        'guestEvents':guestEvents,
        'vendorPending':vendorPending,
        'vendorEvents':vendorEvents
    })
    # View code here...
#n    return render(request, 'RSVP/home.html')

def events_list(request, event_id):
    event = get_object_or_404(Event, pk = event_id)

    questions = Question.objects.filter(event=event)

    guest = RegisterEvent.objects.filter(event=event,identity=2)
    guestPending = guest.filter(register_state=0)
    guestPass = guest.filter(register_state=1)
    guestNum = guestPass.count()

    owner = RegisterEvent.objects.filter(event=event,identity=0)
    ownerPending = owner.filter(register_state=0)
    ownerPass = owner.filter(register_state=1)
    ownerNum = ownerPass.count()

    vendor = RegisterEvent.objects.filter(event=event,identity=1)
    vendorPending = vendor.filter(register_state=0)
    vendorPass = vendor.filter(register_state=1)
    vendorNum = vendorPass.count()

    return render(request, 'RSVP/events_list.html', {
        'event_name': event.event_name,
        'event_time': event.event_time,
        'guestPending':guestPending,
        'guestPass':guestPass,
        'guestNum':guestNum,
        'ownerPending':ownerPending,
        'ownerPass':ownerPass,
        'ownerNum':ownerNum,
        'vendorPending':vendorPending,
        'vendorPass':vendorPass,
        'vendorNum':vendorNum,
        'questions':questions,
        'timeNow':timezone.now()
        
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
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('../../home')
                else:
                    return HttpResponse("this user is not active")
            else:
                return HttpResponse("failed to authenticate")                
    else:
        form = UserCreationForm()
    return render(request, 'RSVP/signup.html', {'form': form})

def test(request):
    return HttpResponse("Hello, world. You're " + request.user.username)
def logout(request):
    logout(request)
    return redirect('../login')
