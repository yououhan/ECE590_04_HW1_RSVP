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
from django.core.exceptions import ObjectDoesNotExist


class QuestionWithResponse:
    #this class is used to create the question
    #with an array of this QuestionWithResponse it is easy to display
    def __init__(self, question, choices, response):
        self.question = question
        self.choices = choices
        self.response = response

        
def questionView(request,event_id,guest_id):
    # this function is the main function of the url:event/<int:event_id>/questionView/<int:guest_id>
    #this function would help the vendor and the owner
    #to view the answer of a guest
    #can call a function accordingly
    event = get_object_or_404(Event,pk = event_id)
    user = request.user
    guest = get_object_or_404(User,pk = guest_id)
    if not isGuest(guest,event):
        return HttpResponse('no such guest in the event')
    if isVendor(user,event):
        return viewAnswer(request,event,guest,False)
    if isOwner(user,event):
        return viewAnswer(request,event,guest,True)
    return render(request,'RSVP/errorPage.html',{'username':user})

def viewAnswer(request,event,guest,ownership):
    # this function is for owner or vendor to view the answer of a guest
    # the owner can see all the answer while vendor can only see the question that is visible
    registerEvent = get_object_or_404(RegisterEvent,event=event,user=guest)
    if ownership:
        question = Question.objects.filter(event=event)   #owner can see
    else:
        question = Question.objects.filter(event=event,isVisible=True)  # vendor can see
    multiChoiceQuestions = question.filter(event=event, question_type='S')
    textQuestions = question.filter(event=event, question_type='T')
    questionWithPlusOneResponses = addAllQuestion(multiChoiceQuestions,textQuestions,registerEvent, True)
    questionWithResponses = addAllQuestion(multiChoiceQuestions,textQuestions,registerEvent, False)
    showPlusOneQuestions = True
    questionIds = Question.objects.values_list('id').filter(event=event, question_type='S')
    choices = Choice.objects.filter(question__in=questionIds)
    return render(request,'RSVP/questionAnswer.html',{
        'username':request.user,
        'choices':choices,
        'multiChoiceQuestions':multiChoiceQuestions,
        'textQuestions':textQuestions,
        'questionWithResponses': questionWithResponses,
        'noSubmit':True,
        'showPlusOneQuestions': showPlusOneQuestions,
        'multiChoiceQuestions':multiChoiceQuestions,
        'questionWithPlusOneResponses': questionWithPlusOneResponses
    })
    
def addAllQuestion(multiChoiceQuestions,textQuestions,registerEvent,isPlusOne):
    # this function is to create an array of QuestionWithResponse
    # with the input of all the question that need to add
    # and the register info (registerEvent)
    # it would return an array that contain all the answer
    # for each question in a event of a guest
    questionWithResponses = []
    for question in multiChoiceQuestions:
        choices = Choice.objects.filter(question=question)
        try:
            response = MultiChoicesResponse.objects.get(question=question, register_event=registerEvent, is_plus_one=isPlusOne)
        except ObjectDoesNotExist:
            response = None
        questionWithResponses.append(QuestionWithResponse(question, choices, response))
    for question in textQuestions:
        choices = Choice.objects.filter(question=question)
        try:
            response = TextResponse.objects.get(question=question, register_event=registerEvent, is_plus_one=isPlusOne)
        except ObjectDoesNotExist:
            response = None
        questionWithResponses.append(QuestionWithResponse(question, None, response))
    return questionWithResponses

def saveResponses(requestPost, multiChoiceQuestions, textQuestions, registerEvent, isPlusOne):
    # is funciton would create responses or update a old responses
    # of all the question for one guest of one event
    for question in multiChoiceQuestions:
        if isPlusOne:
            choice_selected=requestPost.get('plus_one_' + str(question.id))
        else:
            choice_selected=requestPost.get(str(question.id))
        multiChoicesResponse, created = MultiChoicesResponse.objects.update_or_create(
            question=question,
            register_event=registerEvent,
            is_plus_one=isPlusOne,
            defaults={
                'answer': Choice.objects.get(pk=choice_selected),
                'last_updated_time': timezone.now(),
                'is_plus_one': isPlusOne,
            }
        )
        multiChoicesResponse.save()
    for question in textQuestions:
        if isPlusOne:
            answer_selected=requestPost.get('plus_one_' + str(question.id))
        else:
            answer_selected=requestPost.get(str(question.id))
        textResponse, created = TextResponse.objects.update_or_create(
            question=question,
            register_event=registerEvent,
            is_plus_one=isPlusOne,
            defaults={
                'answer': answer_selected,
                'last_updated_time': timezone.now(),
                'is_plus_one': isPlusOne,
            }
        )
        textResponse.save()
    
def questionAnswer(request, event_id):
    # this function is the main function of the url:event/<int:event_id>/questionAnswer
    # it would show all the response of a guest for an event 
    # and if it is a POST it would create or update the response
    # if this event can bring a +1 it would show a button if clicked a new form would show
    # and guest can add a new response for the +1
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    if not isGuest(user,event):
        return render(request,'RSVP/errorPage.html',{'username':user})
    registerEvent = get_object_or_404(RegisterEvent, event=event, user=user, identity='2')
    multiChoiceQuestions = Question.objects.filter(event=event, question_type='S')
    textQuestions = Question.objects.filter(event=event, question_type='T')
    questionWithPlusOneResponses = addAllQuestion(multiChoiceQuestions,textQuestions,registerEvent, True)
    questionWithResponses = addAllQuestion(multiChoiceQuestions,textQuestions,registerEvent, False)
    multiChoiceResponseCount = MultiChoicesResponse.objects.filter(is_plus_one=True).count()
    textResponseCount = TextResponse.objects.filter(is_plus_one=True).count()
    if multiChoiceResponseCount > 0 or textResponseCount > 0:
        showPlusOneQuestions = True
    else:
        showPlusOneQuestions = False
    if request.method == 'POST':
        if request.POST.get('toggleAPlusOne'):
            if request.POST.get('toggleAPlusOne') == "setTrue":
                showPlusOneQuestions = True
            else:
                showPlusOneQuestions = False
                MultiChoicesResponse.objects.filter(register_event=registerEvent, is_plus_one=True).delete()
                TextResponse.objects.filter(register_event=registerEvent, is_plus_one=True).delete()
        elif request.POST.get('submit'):
            if request.POST.get('submit') == 'guest':
                saveResponses(request.POST, multiChoiceQuestions, textQuestions, registerEvent, False)
            elif request.POST.get('submit') == 'plusOne':
                saveResponses(request.POST, multiChoiceQuestions, textQuestions, registerEvent, True)
            return redirect('./')
    questionIds = Question.objects.values_list('id').filter(event=event_id, question_type='S')
    choices = Choice.objects.filter(question__in=questionIds)
    return render(request, 'RSVP/questionAnswer.html',{
        'username':request.user,
        'choices':choices,
        'event': event,
        'showPlusOneQuestions': showPlusOneQuestions,
        'multiChoiceQuestions':multiChoiceQuestions,
        'textQuestions':textQuestions,
        'questionWithResponses': questionWithResponses,
        'questionWithPlusOneResponses': questionWithPlusOneResponses,
        'noSubmit':False
        })


def isOwner(user,event):
    # this function check if the user is the owner of a event
    permission = get_object_or_404(RegisterEvent,event=event,user=user)
    if permission.identity == '0':
        return True
    return False

def isVendor(user,event):
    # this function check if the user is the vendor of a event
    permission = get_object_or_404(RegisterEvent,event=event,user=user)
    if permission.identity == '1':
        return True
    return False

def isGuest(user,event):
    # this function check if the user is the guest of a event
    permission = get_object_or_404(RegisterEvent,event=event,user=user)
    if permission.identity == '2':
        return True
    return False
    
# def questionCreate(QuestionForm,event):
#     # this function would creat and save a new question
#     question_text = QuestionForm.cleaned_data['question_text']
#     question_type = QuestionForm.cleaned_data['question_type']
#     isEditable =  QuestionForm.cleaned_data['isEditable']
#     isOptional =  QuestionForm.cleaned_data['isOptional']
#     isVisible = QuestionForm.cleaned_data['isVisible']
#     question = Question(
#         event=event,
#         question_text=question_text,
#         question_type=question_type,
#         isEditable=isEditable,
#         isOptional=isOptional,
#         isVisible=isVisible
#     )
#     question.save()
#     return question
            
class ChoiceCount:
    # this class is used to save the statistic of each choice
    def __init__(self, choice, count):
        self.choice = choice
        self.count = count
        
class QuestionStatistics:
    # this class is to hold the statistic of each question
    def __init__(self, question, choiceCounts, text_answers):
        self.question = question
        self.choiceCounts = choiceCounts
        self.text_answers = text_answers


def questionCreate(request,event_id):
    # this function is the main function of the url:event/<int:event_id>/question/
    # it would creat and save a new question for a event
    user = request.user
    event = get_object_or_404(Event,pk = event_id)
    if not isOwner(user,event):
        return render(request,'RSVP/errorPage.html',{'username':user})
    if request.method == 'POST':
        QuestionForm = Questionform(request.POST)
        if QuestionForm.is_valid():
            question = QuestionForm.save(commit = False)
            question.event_id = event_id
            question.save()
            #question = questionCreate(QuestionForm,event)
            return redirect('./' + str(question.id))
    else:
        QuestionForm = Questionform()
    return render(request,'RSVP/question.html',{
        'Questionform': QuestionForm,
        'isCreate':'1',
        'username':user
    })
        
    
def questionEdit(request, event_id, question_id):
    # this function is the main fuction of the url:event/<int:event_id>/question/<int:question_id>/
    # it would update the question text or add or delete the choice of that question
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    question = get_object_or_404(Question,pk=question_id)
    if isOwner(user,event):
        return questionEditOwner(request,question, event_id)
    return render(request,'RSVP/errorPage.html',{'username':user})


# def questionEdit(QuestionForm,question):
#     # this funciton is to edit a existed question
#     question_text = QuestionForm.cleaned_data['question_text']
#     question_type = QuestionForm.cleaned_data['question_type']
#     isEditable =  QuestionForm.cleaned_data['isEditable']
#     isOptional =  QuestionForm.cleaned_data['isOptional']
#     question.question_text = question_text
#     question.question_type = question_type
#     question.isEditable = isEditable
#     question.isOptional = isOptional
#     question.save()


def addChoice(newChoiceForm,question):
    # this funciton is to add choice to a question
    newChoiceText = newChoiceForm.cleaned_data.get('choice_text')
    newChoice = Choice(
        question = question,
        choice_text = newChoiceText
    )
    newChoice.save()

def sentEmail(toBeDeleted,question):
    # this function is to sent email to the guest who chose the choice that is deleted
    toSent = MultiChoicesResponse.objects.filter(answer=toBeDeleted)
    emailList = []
    for response in toSent:
        registerinfo = response.register_event
        people = registerinfo.user
        emailList.append(people.email)
    mailMessage = 'the choice '+ toBeDeleted.choice_text +' in the question '+ question.question_text
    mailMessage = mailMessage + ' has been deleted. please login to vcm-3030.vm.duke.edu:8080/RSVP (or vcm-2827.vm.duke.edu:8080/RSVP) to change your answer'
    send_mail(
        'Question Change in YouEeveent',
        mailMessage,
        'yiweiliant@gmail.com',
        emailList,
        fail_silently=False,
    )
    
def questionEditOwner(request,question, event_id):
    # this function is called by the function questionEdit,
    # and should be accessed by the owner
    # it can help the owner to add or delete choice, change or delete question 
    choice = Choice.objects.filter(question=question)
    if request.method == 'POST':
        if request.POST.get('changeQuestion'):
            QuestionForm = Questionform(request.POST)
            if QuestionForm.is_valid():
                question = QuestionForm.save(commit = False)
                question.event_id = event_id
                #questionEdit(QuestionForm,question)             
        elif request.POST.get('add_choice'):
            newChoiceForm = newChoiceform(request.POST)
            if newChoiceForm.is_valid():
                addChoice(newChoiceForm,question)
        elif request.POST.get('delete'):
            toBeDeleted = Choice.objects.get(pk=request.POST.get('delete'))
            sentEmail(toBeDeleted,question)     
            toBeDeleted.delete()
        elif request.POST.get('deleteQ'):
            question.delete()
            return redirect('../../')
    newChoiceForm = newChoiceform()
    QuestionForm = Questionform(instance = question)
    return render(request,'RSVP/question.html',{
        'newChoiceform':newChoiceForm,
        'Questionform': QuestionForm,
        'question':question,
        'choice':choice,
        'username':request.user
    })

def event_create(request):
    # this function is the main function of the url: event_create/
    user = request.user
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit = False)
            event.creator = user
            event.save()
            register=RegisterEvent(event=event,
                                   user=user,
                                   identity = '0',
                                   register_state ='1'#register the creator as the owner of the event
            )
            register.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request,'RSVP/event_create.html',{
        'form':form
    })
        

#testing
# def sign_in(request):
#     Events = Event.objects.all()
    
#     return render(request, 'RSVP/sign_in.html', {
#         'Events': Events,
#     })


def home(request):
    # this function is the main function of the url: /RSVP/home
    # it would show all the event a user have
    # and help the user to accpet or decline a event
    user = get_object_or_404(User,username = request.user.username)
    own =  RegisterEvent.objects.filter(user=user,identity=0)
    ownEventsPending = own.filter(register_state = 0)
    ownEvents = own.filter(register_state = 1)
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


def event_info(request,event_id):
    # is function is the main funciton of the url:RSVP/event/<int:event_id>/
    # which can only be accessed by the vendor and owner
    # and call different funciton accordingly
    user = request.user
    event = get_object_or_404(Event,pk = event_id)
    if isOwner(user,event):
        return event_info_owner(request,event)
    elif isVendor(user,event):
        return event_info_vender(request,event)
    else:
        return render(request,'RSVP/errorPage.html',{'username':user})
    
def countStatistics(questions):
    # this function is used to calculate the statistics of questions
    questionStatisticses = []
    for question in questions:
        if question.question_type == 'S':
            choices = Choice.objects.filter(question=question)
            choiceCounts = []
            for choice in choices:
                count = MultiChoicesResponse.objects.filter(answer=choice).count()
                choiceCounts.append(ChoiceCount(choice, count))
            questionStatisticses.append(QuestionStatistics(question, choiceCounts, None))
        elif question.question_type == 'T':
            textAnswers = TextResponse.objects.filter(question=question)
            questionStatisticses.append(QuestionStatistics(question, None, textAnswers))
    return questionStatisticses


def event_info_vender(request, event):
    # this function is called by event_info, and can should only be accessed by vender
    # it would display all the guests and the statistic of all the questions the user have access
    if request.method == 'POST':
        toBeChangedQuestion = get_object_or_404(Question, pk=request.POST.get("finalize"))       
        toBeChangedQuestion.isEditable = not toBeChangedQuestion.isEditable
        toBeChangedQuestion.save()
    username=request.user.username            
    questions = Question.objects.filter(event=event,isVisible=True).order_by('id')
    guest = RegisterEvent.objects.filter(event=event,identity=2)
    guestPending = guest.filter(register_state=0)
    guestPass = guest.filter(register_state=1)
    guestNum = guestPass.count()
    questionStatisticses = countStatistics(questions)
    return render(request, 'RSVP/event_info.html', {
        'event': event,
        'permission':'1',
        'event_name':event.event_name,
        'guestPending':guestPending,
        'guestPass':guestPass,
        'guestNum':guestNum,
        'questions':questions,
        'timeNow':timezone.now(),
        'username':username,
        'questionStatisticses': questionStatisticses
    })


    
def event_info_owner(request, event):
    # this function is called by event_info, and can should only be accessed by owner
    # it display all the list of owner vendor guest and question
    # it can help the owner add new question
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
                    event=event,
                    user = new_user,
                    identity= request.POST.get('invite'),
                    register_state='0'
                    )
                try:
                    newInvite.save()
                except:
                    return HttpResponse("can not invite same people twice")###############error page!
    username=request.user.username            
    questions = Question.objects.filter(event=event)

    guest = RegisterEvent.objects.filter(event=event,identity='2')
    guestPending = guest.filter(register_state=0)
    guestPass = guest.filter(register_state=1)
    guestNum = guestPass.count()

    owner = RegisterEvent.objects.filter(event=event,identity='0')
    ownerPending = owner.filter(register_state=0)
    ownerPass = owner.filter(register_state=1)
    ownerNum = ownerPass.count()

    vendor = RegisterEvent.objects.filter(event=event,identity='1')
    vendorPending = vendor.filter(register_state=0)
    vendorPass = vendor.filter(register_state=1)
    vendorNum = vendorPass.count()
    inviteNewUserForm = inviteNewUserform()
    
    return render(request, 'RSVP/event_info.html', {
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


def signup(request):
    # sign up page
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
                    return redirect('home')
                else:
                    return HttpResponse("this user is not active")
            else:
                return HttpResponse("failed to authenticate")                
    else:
        form = UserCreationForm()
    return render(request, 'RSVP/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/RSVP')
