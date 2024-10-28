from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.about_club_page, name='about club page'),
    path('home', views.about_club_page, name='about club page'),
    path('about', views.about_club_page, name='about club page'),
]
