from django.urls import path

from . import views

urlpatterns = [
    path('sign_in', views.sign_in, name='sign_in'),
    path('home', views.home, name='home'),
    path('<int:event_id>/', views.events_list, name='events_list'),
    path('index', views.index, name = 'index'),
    path('sign_up', views.sign_up, name = 'sign_up')
]
