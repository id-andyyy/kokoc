from django.urls import path
from . import views

urlpatterns = [
    path('populate_matches', views.populate_matches, name='populate_matches'),
    path('populate_old_matches', views.populate_old_matches, name='populate_matches'),
    path('populate_next_matches', views.populate_next_matches, name='populate_matches'),
    path('populate_team', views.populate_team, name='populate_teams'),
    path('populate_coaches', views.populate_coaches, name='populate coaches')
]
