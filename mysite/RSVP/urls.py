from django.urls import path,include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('questionPage',views.questionPage,name='questionPage'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('home/', views.home, name='home'),
    path('event/<int:event_id>', views.events_list, name='events_list'),
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
