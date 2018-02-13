from django.urls import path,include,re_path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', auth_views.LoginView.as_view(template_name='RSVP/login.html', redirect_authenticated_user = True), name = 'login'),
    path(r'logout/', views.logout_view, name = 'logout'),
    path(r'signup/', views.signup, name = 'signup'),
    path('home/', views.home, name='home'),
    path('event_create/', views.event_create, name='event create'),       
    # access to owner and vender but have different view
    path('event/<int:event_id>/', views.event_info, name='event detail'),
    # for new question create, only access to owner
    path('event/<int:event_id>/question/',views.questionCreate,name='question create'),
    # for question edit and add choive, only access to owner 
    path('event/<int:event_id>/question/<int:question_id>/',views.questionEdit,name='question edit'),
    # access to owner and vendor, but vendor can only view limit question
    path('event/<int:event_id>/questionView/<int:guest_id>',views.questionView,name='questionView'),
    # for guest to answer question only access to guest
    path('event/<int:event_id>/questionAnswer/',views.questionAnswer,name='question answer'),
]
    
