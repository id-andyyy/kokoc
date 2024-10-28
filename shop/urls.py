
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('shop', views.shop, name='shop'),
    path('shop/product/', views.product_page, name='product page'),
    path('clear_photos', views.clear_photos, name='product page')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)