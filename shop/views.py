from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main.models import Shop
from django.core.files.storage import default_storage
from urllib3 import request


def shop(request):
    shop = Shop.objects.all()
    attrs = {
        'shop': shop
    }
    return render(request, 'shop.html', attrs)


async def is_admin(user):
    return user.is_authenticated and user.profile.role == 'admin'


@login_required
def clear_photos(request):
    if not is_admin(request.user):
        return redirect('/home')
    clean_unused_photos()
    return redirect('/home')


def clean_unused_photos(folder='shop_photos'):
    used_photos = set()
    for shop_item in Shop.objects.all():
        for field_name in ('photo1', 'photo2', 'photo3'):
            photo_path = getattr(shop_item, field_name)
            if photo_path:
                used_photos.add(photo_path.name)
    unused_photos = set()
    for filename in default_storage.listdir(folder)[1]:
        if f'{folder}/{filename}' not in used_photos:
            unused_photos.add(filename)
    for filename in unused_photos:
        full_path = default_storage.path(f'{folder}/{filename}')
        if default_storage.exists(full_path):
            default_storage.delete(full_path)
            # print(f'Удален неиспользуемый файл: {filename}')


def product_page(request):
    id = request.GET.get('id')
    try:
        profile = request.user.profile
        points = profile.points
        product = Shop.objects.get(id=id)
        attrs = {
            'product': product,
            'points': points
        }
        return render(request, 'product.html', attrs)
    except:
        product = Shop.objects.get(id=id)
        attrs = {
            'product': product,
            'points': 0
        }
        return render(request, 'product.html', attrs)
