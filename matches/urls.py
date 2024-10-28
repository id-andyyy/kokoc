from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('matches', views.matches, name='matches 2'),
    path('matches-info/<int:id>', views.matches_info, name='matches info'),
    path('next-matches-info/<int:id>', views.next_matches_info, name='next matches info')
]
