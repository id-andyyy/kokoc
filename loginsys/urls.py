from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from loginsys import views

urlpatterns = [
    path('sign_up', views.sign_up, name='sign_up'),
    path('log_out', views.log_out, name='log_out'),
    path('log_in', views.log_in, name='log_in'),
    path('profile', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit_profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
