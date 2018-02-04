from django.urls import path

from . import views

urlpatterns = [
    path('sign_in', views.sign_in, name='sign_in'),
    path('home/<int:people_id>', views.home, name='home'),
    path('event/<int:event_id>', views.events_list, name='events_list'),
    path('index', views.index, name = 'index'),
    path('sign_up', views.sign_up, name = 'sign_up')
]
