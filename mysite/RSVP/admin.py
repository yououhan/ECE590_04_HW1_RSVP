from django.contrib import admin

# Register your models here.
from .models import People, Event, Question, RegisterEvent, Response, EventAccess, QuestionAccess

admin.site.register(People)
admin.site.register(Event)
admin.site.register(Question)
admin.site.register(RegisterEvent)
admin.site.register(Response)
admin.site.register(EventAccess)
admin.site.register(QuestionAccess)
