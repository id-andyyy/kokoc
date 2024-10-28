from asgiref.sync import sync_to_async
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from loginsys.forms import RegisterForm, LoginForm, ProfileForm, UserForm, CustomPasswordChangeForm
from loginsys.models import Profiles


@sync_to_async()
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('confirm_password')
        if not name or not email or not password or not password1:
            messages.error(request, 'Все поля должны быть заполнены.')
            return render(request, 'loginsys/sign_up.html', {'form': form,
                                                             'name': name,
                                                             'email': email,
                                                             'password': password,
                                                             'password1': password1,
                                                             'title': 'sign_up'
                                                             })
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким электронным адресом уже существует.')
            return render(request, 'loginsys/sign_up.html', {'form': form,
                                                             'name': name,
                                                             'email': email,
                                                             'password': password,
                                                             'password1': password1,
                                                             'title': 'sign_up'
                                                             })
        if password != password1:
            messages.error(request, 'Пароли не совпадают.')
            return render(request, 'loginsys/sign_up.html', {'form': form,
                                                             'name': name,
                                                             'email': email,
                                                             'password': password,
                                                             'password1': password1,
                                                             'title': 'sign_up'
                                                             })
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()
        profile = Profiles.objects.create(user=user, points=0)
        profile.save()

        login(request, user)
        return redirect('/home')
    form = RegisterForm
    return render(request, 'loginsys/sign_up.html', {'form': form, 'title': 'sign_up'})


@sync_to_async()
def log_in(request):
    if request.user.is_authenticated:
        return redirect('/home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Пользователь с такой электронной почтой не найден')
            return render(request, 'loginsys/login.html', {'form': form, 'email': email, 'title': 'login'})
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, 'Неверный пароль')
            return render(request, 'loginsys/login.html', {'form': form, 'email': email, 'title': 'login'})
    else:
        form = LoginForm()
        return render(request, 'loginsys/login.html', {'form': form, 'title': 'login'})


@sync_to_async()
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/home')


@login_required()
@sync_to_async
def profile(request):
    profile = Profiles.objects.get(user=request.user)
    name = request.user.first_name
    email = request.user.email
    date = profile.birthdate
    if date is None:
        date = 'Не указано'
    date_joined = profile.data_joined
    return render(request, 'loginsys/profile.html',
                  {'email': email, 'name': name, 'date': date, 'date_joined': date_joined, 'title': 'profile',
                   'profile': profile})


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if 'update_profile' in request.POST:
            if profile_form.is_valid() and user_form.is_valid():
                profile_form.save()
                user_form.save()
                messages.success(request, 'Профиль успешно обновлён!')
                return redirect('/profile')
        elif 'update_password' in request.POST:
            if password_form.is_valid():
                if request.user.check_password(request.POST['old_password']):
                    if request.POST['new_password1'] == request.POST['new_password2']:
                        password_form.save()
                        update_session_auth_hash(request, password_form.user)
                        messages.success(request, 'Пароль успешно изменён!')
                        return redirect('/profile')
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
    flag = True
    context = {
        'message': messages,
        'profile_form': profile_form,
        'user_form': user_form,
        'password_form': password_form,
        'flag': flag,
    }
    return render(request, 'loginsys/edit_profile.html', context)
