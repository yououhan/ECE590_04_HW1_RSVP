from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from .models import *
from django.core.exceptions import ObjectDoesNotExist
class QuestionWithResponse:
    #this class is used to create the question
    #with an array of this QuestionWithResponse it is easy to display
    def __init__(self, question, choices, response):
        self.question = question
        self.choices = choices
        self.response = response

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
        try:
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
        except:
            pass
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
    
