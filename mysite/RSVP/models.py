from django.db import models

QUESTION_TEXT_MAX_LENGTH = 200
EVENT_NAME_MAX_LENGTH = 100
QUESTION_TYPES_CHOICES = (
    ('S', 'Single select'),
    ('M', 'Multiple select'),
    ('T', 'Text')
)
# Create your models here.
class Question(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete = models.CASCADE
        )
    question_text = models.CharField(max_length = QUESTION_TEXT_MAX_LENGTH)
    question_type = model.CharField(max_length = 1, choices = QUESTION_TYPES_CHOICES)
    isEditable = models.BooleanField(default = True)
    isOptional = models.BooleanField(default = False)
    last_updated_time = models.DateTimeField('last updated time', auto_now = True)
    
class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE#When the referenced object is deleted, also delete the objects that have references to it (When you remove a blog post for instance, you might want to delete comments as well).
        )
    choice_text = 

class Event(models.Model):
    event_name = models.CharField(max_length = EVENT_NAME_MAX_LENGTH)
    creator = models.ForeignKey(
        People,
        on_delete=models.SET_NULL#Set the reference to NULL (requires the field to be nullable). For instance, when you delete a User, you might want to keep the comments he posted on blog posts, but say it was posted by an anonymous (or deleted) user.
        )
    create_time = models.DateTimeField('time created', auto_now_add = True)
    last_updated_time = models.DateTimeField('last updated time', auto_now = True)

class People(models.Model):
    username = models.CharField(max_length = PEOPLE_USERNAME_MAX_LENGTH)
    name = models.CharField(max_length = PEOPLE_NAME_MAX_LENGTH)
    password = 
    hashString

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
    identity#0: owner, 1: vendor, 2: guest
    state#0: pending, 1: passed, 2: declined_unread, 3: declined_read

class Response(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
        )
    guest = models.ForeginKey(
        People,
        on_delete=models.CASCADE
        )
    answer = #???? is choice a foreign key of answer??
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
    access 
