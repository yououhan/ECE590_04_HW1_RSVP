from django.contrib import admin

# Register your models here.
from .models import People, Event, Question, RegisterEvent, MultiChoicesResponse, TextResponse, EventAccess, QuestionAccess, Choice

admin.site.register(People)
admin.site.register(Event)
admin.site.register(Question)
admin.site.register(RegisterEvent)
admin.site.register(MultiChoicesResponse)
admin.site.register(TextResponse)
admin.site.register(EventAccess)
admin.site.register(QuestionAccess)
admin.site.register(Choice)
