from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('news', views.news, name='news'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('news/<int:news_id>/comment/', views.add_comment, name='add_comment'),
    path('news/like/<int:news_id>/', views.like_post, name='like_post'),
    path('news/comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment')
]
