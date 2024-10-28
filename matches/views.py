import datetime
from calendar import month
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from main.models import Matches, NextMatches
from bs4 import BeautifulSoup as bs


def nearest_match():
    pass


def matches(request):
    flag = False
    k = 0
    while not flag:
        next_matches = NextMatches.objects.all().order_by('date')[k]
        next_match_datetime = datetime.datetime.combine(next_matches.date, next_matches.time)
        if datetime.datetime.now() - next_match_datetime > timedelta(hours=2):
            next_matches.delete()
            k += 1
        else:
            flag = True
    if next_matches.link:
        link = next_matches.link
    else:
        link = None
    next_match = {
        'time': next_match_datetime,  # Следующий матч через день
        'video_url': link,
        'team1_name': 'Кокос Групп',
        'team2_name': next_matches.opponent,
        'team1_logo': "{% static 'img/kokoc_logo.png' %}",
        'team2_logo': next_matches.logo1,
        'id': next_matches.id,
    }

    matches = Matches.objects.all()
    attrs = {
        'next_match': next_match,
        'matches': matches,
    }
    return render(request, 'matches.html', attrs)


def matches_info(request, id):
    match = Matches.objects.get(id=id)
    if 'youtube' in match.link:
        source = 'youtube'
    elif 'vk' in match.link:
        source = 'vk'
        match.link = match.link[:-1] + '0'
    attrs = {
        'match': match,
        'source': source,
    }
    return render(request, 'match_view.html', attrs)


def next_matches_info(request, id):
    match = NextMatches.objects.get(id=id)
    attrs = {
        'match': match,
    }
    return render(request, 'match_view.html', attrs)
