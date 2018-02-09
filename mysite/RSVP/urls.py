from django.urls import path,include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('event/<int:event_id>/questionPage/<int:question_id>',views.questionPageEdit,name='questionPageEdit'),
#    path('event/<int:event_id>/questionFinalize/<int:question_id>',views.questionFinalize,name='questionFinalize'),
    path('event/<int:event_id>/questionPage/',views.questionPageCreate,name='questionPageCreate'),
    path('event/<int:event_id>/questionAnswer/',views.questionAnswer,name='questionAnswer'),
    path('event/<int:event_id>/questionView/<int:guest_id>',views.questionAnswer,name='questionAnswer'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('home/', views.home, name='home'),
    path('event/<int:event_id>/', views.events_list, name='events_list'),
    path('event_create/', views.event_create, name='event create'),    
    path('index', views.index, name = 'index'),
    path('sign_up', views.sign_up, name = 'sign_up'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='RSVP/login.html')),
    path('accounts/logout/', views.logout,name = 'logout'),
    path('accounts/signup/', views.signup, name = 'signup'),
    path('accounts/test/', views.test, name = 'test'),
#    path('accounts/profile/', views.test, name = 'profile'),
    #    path('accounts/', auth_views.login, name = 'login'),
]
