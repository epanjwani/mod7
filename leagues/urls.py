from django.urls import path
from . import views

app_name = 'leagues'
urlpatterns = [path('', views.home, name='home'),
path('welcome', views.welcomePage, name='welcome'),
path('signup', views.signUp, name='signup'),
path('login', views.login, name='login'),
path('logout', views.logout, name='logout'),
path('createleague', views.createLeague, name ='createleague'),
path('enterteams', views.enterteams, name='enterteams'),
path('enterdata1', views.enterdata1, name='enterdata1')]
