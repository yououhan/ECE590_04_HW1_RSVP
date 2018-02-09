from django.urls import path,include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='RSVP/login.html')),
    path('accounts/logout/', views.logout,name = 'logout'),
    path('accounts/signup/', views.signup, name = 'signup'),
    path('home/', views.home, name='home'),
    
    path('event_create/', views.event_create, name='event create'),    
   
    path('event/<int:event_id>/', views.events_list, name='events_list'),
    # access to owner and vender but have different view
    path('event/<int:event_id>/questionPage/',views.questionPageCreate,name='questionPageCreate'),
    # for new question create, only access to owner
    path('event/<int:event_id>/questionPage/<int:question_id>/',views.questionPageEdit,name='questionPageEdit'),
    # for question edit and add choive, only access to owner 
    path('event/<int:event_id>/questionView/<int:guest_id>',views.questionAnswer,name='questionAnswer'),
    # access to owner and vender, but vender can only view limit question
    path('event/<int:event_id>/questionStatistics/',views.questionStatistics,name='questionStatistics'),
    # for vender use will mergo the the event/<int:event_id> page soon
    path('event/<int:event_id>/questionAnswer/',views.questionAnswer,name='questionAnswer'),
    # for guest to answer question only access to guest

    path('sign_in', views.sign_in, name='sign_in'),
    path('index', views.index, name = 'index'),
    path('sign_up', views.sign_up, name = 'sign_up'),
    path('accounts/test/', views.test, name = 'test'),
#    path('accounts/profile/', views.test, name = 'profile'),
    #    path('accounts/', auth_views.login, name = 'login'),
]
