from django.contrib import admin

# Register your models here.
from .models import Event, Question, RegisterEvent, MultiChoicesResponse, TextResponse, Choice

admin.site.register(Event)
admin.site.register(Question)
admin.site.register(RegisterEvent)
admin.site.register(MultiChoicesResponse)
admin.site.register(TextResponse)
admin.site.register(Choice)
