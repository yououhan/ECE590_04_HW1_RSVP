import django
from django.conf import settings
from django.shortcuts import get_object_or_404, render,redirect
from .models import Event,RegisterEvent,Question, Choice, MultiChoicesResponse, TextResponse
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import logout
from .forms import EventForm, Questionform, Choiceform
from django.forms import formset_factory
from .forms import UserCreationForm, inviteNewUserform,newChoiceform, TextResponseform
from django import forms
from django.core.mail import send_mail
from django.forms import inlineformset_factory

def makeMultiChoiceAnswerform(question):
    choicesQueryset = Choice.objects.filter(question=question.id)
    class multiChoiceAnswerform(forms.Form):
        question_text = forms.CharField(widget=forms.TextInput(attrs={'placeholder': question.question_text}),disabled = True, label=False)
        choices = forms.ModelChoiceField(queryset=choicesQueryset)
    return multiChoiceAnswerform

def questionAnswerView(request,event_id,guest_id):
    user = request.user
    event=get_object_or_404(Event,pk = event_id)
    permission = get_object_or_404(RrgisterEvent,event=event,user=user)
    if permission.identity == '2':
        return questionAnswer(request,event_id)
    else:
        return questionAnserAll(request,event_id,guest_id,permission.identity)

def questionAnswerAll(request,event_id,guest_id,permission):
    user=request.user
    event=get_object_or_404(Event,pk=event_id)
    guest=get_object_or_404(User,pk=guest_id)
    guestAccess=get_object_or_404(RegisterEvnet,event=event,user=guest)
    if guestAccess == '2':
#        return 
#    else:
        return HttpResponse('seems that the guest is not in this event')
    
def questionAnswer(request, event_id):
    multiChoiceQuestions = Question.objects.filter(event=event_id, question_type='S')
    textQuestions = Question.objects.filter(event=event_id, question_type='T')
#    textResponseFormSet = inlineformset_factory(Event, Question, fields=('question_text',))
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        registerEvent = get_object_or_404(RegisterEvent, event=event, user=request.user, identity='2')
        for question in multiChoiceQuestions:
            multiChoicesResponse = MultiChoicesResponse(
                question = question,
                register_event=registerEvent,
                answer = Choice.objects.get(pk=request.POST.get(str(question.id))),
                last_updated_time = timezone.now()
            )
            multiChoicesResponse.save()
        for question in textQuestions:
            textResponse = TextResponse(
                question = question,
                register_event = registerEvent,
                answer = request.POST.get(str(question.id)),
                last_updated_time = timezone.now()
            )
            textResponse.save()
        return redirect('../../../home')
    questionIds = Question.objects.values_list('id').filter(event=event_id, question_type='S')
#    questionIds = Question.objects.values_list('id').filter(event=event_id, question_type='S')
#    question = multiChoiceQuestions.first()
#    MultiChoiceAnswerFormset = formset_factory(MultiChoiceAnswerform)
#    for question in multiChoiceQuestions:
    choices = Choice.objects.filter(question__in=questionIds)
#    textResponseFS = textResponseFormSet(instance=event)
#    return HttpResponse(textResponseFS)
    #formset = QuestionFormSet(instance=question)
#    multiChoiceAnswerForm = makeMultiChoiceAnswerform(question)
#        addToFormset(multiChoiceAnswerForm)
    return render(request, 'RSVP/questionAnswer.html',{
        'choices':choices,
        'multiChoiceQuestions':multiChoiceQuestions,
        'textQuestions':textQuestions,
#        'textResponseFormSet':textResponseFS,
#        'multiChoiceQuestions':multiChoiceQuestions,
#        'multiChoiceAnswerform':formset,#multiChoiceAnswerForm,
 #       'multiChoiceAnswerformset':multiChoiceAnswerFormset,
        })

def questionPageCreate(request,event_id):
    if request.method == 'POST':
        QuestionForm = Questionform(request.POST)
        if QuestionForm.is_valid():
            question_text = QuestionForm.cleaned_data['question_text']
            question_type = QuestionForm.cleaned_data['question_type']
            isEditable =  QuestionForm.cleaned_data['isEditable']
            isOptional =  QuestionForm.cleaned_data['isOptional']
            isVisible = QuestionForm.cleaned_data['isVisible']
            question = Question(
                event= get_object_or_404(Event,pk = event_id),
                question_text=question_text,
                question_type=question_type,
                isEditable=isEditable,
                isOptional=isOptional,
                isVisible=isVisible
            )
            question.save()
            return redirect('..')
            
    else:
        QuestionForm = Questionform()
    return render(request,'RSVP/questionPage.html',{
        'Questionform': QuestionForm,
        
    })

def questionPageEdit(request, event_id, question_id):
    question = get_object_or_404(Question,pk=question_id)
    choice = Choice.objects.filter(question=question)
    if request.method == 'POST':
        if request.POST.get('changeQuestion'):
            QuestionForm = Questionform(request.POST)
            if QuestionForm.is_valid():
                question_text = QuestionForm.cleaned_data['question_text']
                question_type = QuestionForm.cleaned_data['question_type']
                isEditable =  QuestionForm.cleaned_data['isEditable']
                isOptional =  QuestionForm.cleaned_data['isOptional']
                question = Question.objects.get(pk = question_id)
                question.question_text = question_text
                question.question_type = question_type
                question.isEditable = isEditable
                question.isOptional = isOptional
                question.save()
        elif request.POST.get('add_choice'):
            newChoiceForm = newChoiceform(request.POST)
            if newChoiceForm.is_valid():
                newChoiceText = newChoiceForm.cleaned_data.get('choice_text')
                newChoice = Choice(
                question = question,
                choice_text = newChoiceText
                )
                newChoice.save()
        elif request.POST.get('delete'):
            toBeDeleted = Choice.objects.get(pk=request.POST.get('delete'))
            mailMessage = 'the choice '+ toBeDeleted.choice_text +' in the question '+ question.question_text
            send_mail(
                'Is that easy?',
                mailMessage,
                'yiweiliant@gmail.com',
                ['yiweiliant@outlook.com'],
                fail_silently=False,
            )
            toBeDeleted.delete()
        elif request.POST.get('deleteQ'):
            toDeleteQuestion = Question.objects.get(pk=question_id)
            toDeleteQuestion.delete()
            return redirect('../')
            
    newChoiceForm = newChoiceform()
    QuestionForm = Questionform(instance = question)
    return render(request,'RSVP/questionPage.html',{
        'newChoiceform':newChoiceForm,
        'Questionform': QuestionForm,
        'question':question,
        'choice':choice,
    })
    
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event_name = form.cleaned_data['event_name']
            event_time = form.cleaned_data['event_time']
            creator = request.user
            event = Event(event_name=event_name,
                          event_time=event_time,
                          creator = creator
            )
            event.save()
            register=RegisterEvent(event=event,
                                   user=request.user,
                                   identity = '0',
                                   register_state ='1' 
            )
            register.save()
            if form.cleaned_data['plusOne']:
                question=Question(event=event,
                                  question_text="will you have anyone come with you?",
                                  question_type='S'
                )
                question.save()
                no=Choice(question=question,
                          choice_text="NO"
                )
                no.save()
                yes=Choice(question=question,
                           choice_text="YES"
                )
                yes.save()
            return redirect('../home')
    else:
        form = EventForm()
    #form.fields['event_name'].widget.attrs['readonly'] = True # disable a form!
    return render(request,'RSVP/event_create.html',{
        'form':form
    })
        

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
    if request.method == 'POST':
        if request.POST.get('accept'):
            acceptRegister=RegisterEvent.objects.get(pk=request.POST.get('accept'))
            acceptRegister.register_state='1'
            acceptRegister.save()
        elif request.POST.get('decline'):
            declineRegister=RegisterEvent.objects.get(pk=request.POST.get('decline'))
            declineRegister.register_state='2'
            declineRegister.save()
    return render(request,'RSVP/home.html',{
        'username' : user.username,
        'ownEventsPending': ownEventsPending,
        'ownEvents':ownEvents,
        'guestPending':guestPending,
        'guestEvents':guestEvents,
        'vendorPending':vendorPending,
        'vendorEvents':vendorEvents,
        'timeNow':timezone.now()
    })
    # View code here...
#n    return render(request, 'RSVP/home.html')
def events_list(request,event_id):
    user = request.user
    event = get_object_or_404(Event,pk = event_id)
    permission = get_object_or_404(RegisterEvent,event=event,user=user)
    if permission.identity == '0':
        return events_list_owner(request,event)
    elif permission.identity == '1':
        return events_list_vender(request,event)
    else:
        return HttpResponse('you have on access to this page(will be better)')



def events_list_vender(request, event):

    username=request.user.username            
    questions = Question.objects.filter(event=event)

    guest = RegisterEvent.objects.filter(event=event,identity=2)
    guestPending = guest.filter(register_state=0)
    guestPass = guest.filter(register_state=1)
    guestNum = guestPass.count()

    return render(request, 'RSVP/events_list.html', {
        'event': event,
        'permission':'1',
        'event_name':event.event_name,
        'guestPending':guestPending,
        'guestPass':guestPass,
        'guestNum':guestNum,
        'questions':questions,
        'timeNow':timezone.now(),
        'username':username,
    })


    
def events_list_owner(request, event):
    if request.method == 'POST':
        if request.POST.get('delete_event'):
            event.delete()
            return redirect('../../home/')
        elif request.POST.get('invite'):
            inviteNewUserForm = inviteNewUserform(request.POST)
            if inviteNewUserForm.is_valid():
                new_userName = inviteNewUserForm.cleaned_data.get('username')
                new_user=User.objects.get(username=new_userName)
                newInvite=RegisterEvent(
                    event=get_object_or_404(Event,pk=event_id),
                    user = new_user,
                    identity= request.POST.get('invite'),
                    register_state='0'
                )
                newInvite.save()
    username=request.user.username            
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
    inviteNewUserForm = inviteNewUserform()
    
    return render(request, 'RSVP/events_list.html', {
        'event': event,
        'permission':'0',
        'event_name':event.event_name,
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
        'timeNow':timezone.now(),
        'username':username,
        'inviteNewUserform':inviteNewUserForm,
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
