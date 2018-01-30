from django.db import models
from django.db.models import CharField, Model
from django_mysql.models import ListCharField


QUESTION_TEXT_MAX_LENGTH = 200
CHOICE_TEXT_MAX_LENGTH = 200
CHOICE_MAX_NUMBER = 10;
EVENT_NAME_MAX_LENGTH = 100
PEOPLE_USERNAME_MAX_LENGTH = 20
PEOPLE_NAME_MAX_LENGTH = 20
QUESTION_TYPES_CHOICES = (
    ('S', 'Single select'),
    ('M', 'Multiple select'),
    ('T', 'Text')
)
IDENTITY_CHOICES = (
    ('0', 'Owner'),
    ('1', 'Vendor'),
    ('2', 'Guest')
)
REGISTER_STATE_CHOICES = (
    ('0', 'Pending'),
    ('1', 'Passed'),
    ('2', 'Declined and unread'),
    ('3', 'Declined and read')
)    
# Create your models here.
class People(models.Model):
    username = models.CharField(max_length = PEOPLE_USERNAME_MAX_LENGTH)
    name = models.CharField(max_length = PEOPLE_NAME_MAX_LENGTH)
#    password = 
#    hashString

class Event(models.Model):
    event_name = models.CharField(max_length = EVENT_NAME_MAX_LENGTH)
    creator = models.ForeignKey(
        People,
        null = True,
        on_delete=models.SET_NULL#Set the reference to NULL (requires the field to be nullable). For instance, when you delete a User, you might want to keep the comments he posted on blog posts, but say it was posted by an anonymous (or deleted) user.
        )
    create_time = models.DateTimeField('time created', auto_now_add = True)
    last_updated_time = models.DateTimeField('last updated time', auto_now = True)

class Question(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete = models.CASCADE
        )
    question_text = models.CharField(max_length = QUESTION_TEXT_MAX_LENGTH)
    question_type = models.CharField(max_length = 1, choices = QUESTION_TYPES_CHOICES)
    isEditable = models.BooleanField(default = True)
    isOptional = models.BooleanField(default = False)
    last_updated_time = models.DateTimeField('last updated time', auto_now = True)
    choices = ListCharField(
        base_field = CharField(max_length = CHOICE_TEXT_MAX_LENGTH),
        size = CHOICE_MAX_NUMBER,
        max_length= ((CHOICE_TEXT_MAX_LENGTH + 1)* CHOICE_MAX_NUMBER)
        )

        
#class Choice(models.Model):
#    question = models.ForeignKey(
#        Question,
#        on_delete=models.CASCADE#When the referenced object is deleted, also delete the objects that have references to it (When you remove a blog post for instance, you might want to delete comments as well).
#        )
#    choice_text = models.CharField(max_length = CHOICE_TEXT_MAX_LENGTH)

class RegisterEvent(models.Model):
    event = models.ForeignKey(#same event can not be registered twice by the same people!!!
        Event,
        on_delete=models.CASCADE
        )
    people = models.ForeignKey(
        People,
        on_delete=models.CASCADE
        )
    register_time = models.DateTimeField('time registered')
    identity = models.CharField(max_length = 1, choices = IDENTITY_CHOICES)
    register_state = models.CharField(max_length = 1, choices = REGISTER_STATE_CHOICES)

class Response(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
        )
    guest = models.ForeignKey(
        People,
        on_delete=models.CASCADE
        )
#    answer = #???? is choice a foreign key of answer??
    last_updated_time = models.DateTimeField('last updated time')

class EventAccess(models.Model):
    registerEvent = models.ForeignKey(
        RegisterEvent,
        on_delete=models.CASCADE#Must be vendor, if the identity is changed, need to manually delte!!!!!!!
        )
    guestNumberIsVisible = models.BooleanField()
    guestListIsVisible = models.BooleanField()

class QuestionAccess(models.Model):
    registerEvent = models.ForeignKey(
        RegisterEvent,
        on_delete=models.CASCADE#Must be vendor, if the identity is changed, need to manually delte!!!!!!!
        )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
        )
    access = models.BooleanField()
