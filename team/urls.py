from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('team/', views.team, name='team'),
    path('player_info/', views.player_info, name='player info')
]
