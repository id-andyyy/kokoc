import asyncio

import aiohttp
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Matches, Team, Articles, Representatives, NextMatches
import requests
from bs4 import BeautifulSoup
from asgiref.sync import sync_to_async
import urllib3
import lxml
import cchardet

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_player_list():
    url = 'https://lfl.ru/club232/players_list'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_='player_title')
    players_names = soup.find_all('p', class_='player_title_name')
    players_logos = soup.find_all('div', class_='player_logo')
    players_card = soup.find_all('div', class_='player_title')
    players = []
    for i in range(len(players_names)):
        dict1 = {}
        dict1['player_name'] = players_names[i].text
        dict1['player_logo'] = players_logos[i].find('a')['href']
        test = players_card[i].find_all('p', class_='')
        dict1['role'] = test[0].text[8:]
        dict1['age'] = int(test[1].text[9:])
        birthday_date = test[2].text[15:].split('.')
        birthday_date = birthday_date[2] + '-' + birthday_date[1] + '-' + birthday_date[0]
        dict1['birthday_date'] = birthday_date
        try:
            dict1['number_on_tshirt'] = int(test[3].text[16:])
        except IndexError:
            dict1['number_on_tshirt'] = 0
        players.append(dict1)
    return players


async def fetch(session, url):
    async with session.get(url, ssl=False) as response:
        return await response.text()


async def get_coach_name():
    url = 'https://lfl.ru/club232/players_list'
    async with aiohttp.ClientSession() as session:
        response_text = await fetch(session, url)
        soup = BeautifulSoup(response_text, 'lxml')
        coaches_names = soup.find_all('span', class_='team_player')
        coaches = []

        tasks = []
        for i in range(len(coaches_names)):
            coach_url = f"https://lfl.ru{coaches_names[i].find('a')['href']}"
            tasks.append(fetch(session, coach_url))

        coach_pages = await asyncio.gather(*tasks)

        for page in coach_pages:
            soup1 = BeautifulSoup(page, 'lxml')
            dict1 = {}
            coach_name = soup1.find_all('p', class_='player_title_name')
            coach_logo = soup1.find_all('div', class_='player_logo')
            coach_title = soup1.find_all("div", class_="player_title")
            coach_age = coach_title[0].find_all("p", class_='')

            dict1["couch_name"] = coach_name[0].text
            dict1['coach_logo'] = coach_logo[0].find("a")["href"]
            dict1['age'] = int(str(coach_age[0])[19:21])
            birthday = str(coach_age[1])[25:35].split('.')
            dict1["birthday"] = f"{birthday[2]}-{birthday[1]}-{birthday[0]}"
            coaches.append(dict1)

    return coaches


def get_matches(played='played', sort='time'):
    url = f'https://lfl.ru/club232/calendar?matches={played}&sort={sort}'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'lxml')
    matches = soup.find_all('tr', class_='white_line')
    all_games = []
    for i in matches:
        about_matches = i.find_all('a')
        dict1 = {}
        logo1 = ''
        flag = False
        k = 0
        for f in about_matches:
            fhref = f['href']
            if logo1 == '' and f.find_all('img'):
                if 'кокос' not in f.text.lower():
                    logo1 = f.find('img')['src']
                    dict1['logo1'] = logo1
                    dict1['opponent'] = f.text
                else:
                    flag = True
            elif 'uzao/tv' in fhref:
                video = 'https://lfl.ru/' + fhref
                url1 = video
                response1 = requests.get(url1, verify=False)
                dict1['video'] = BeautifulSoup(response1.text, 'lxml').find('iframe')['src']
            elif 'stadium' in fhref:
                dict1['stadium'] = f.text
            elif 'tournament' in fhref:
                dict1['tournament'] = f.text
            elif 'match' in fhref:
                if k == 0:
                    date = f.text[:-5].split('.')
                    date = date[2] + '-' + date[1] + '-' + date[0]
                    dict1['date'] = date
                    dict1['day_of_week'] = f.text[-3:-1]
                elif k == 1:
                    dict1['time'] = f.text
                elif k == 2:
                    if flag:
                        try:
                            score = f.text.strip().split(':')
                            score = score[0] + ':' + score[1]
                        except IndexError:
                            pass
                    else:
                        score = f.text.strip()
                    dict1['score'] = score
                k += 1
        all_games.append(dict1)
    return all_games


async def is_admin(user):
    return user.is_authenticated and user.profile.role == 'admin'


@login_required
@sync_to_async
def populate_team(request):
    if not is_admin(request.user):
        return redirect('/home')

    players = get_player_list()
    for player in players:
        team_player, created = Team.objects.get_or_create(
            name=player['player_name'],
            defaults={
                'photo': player['player_logo'],
                'birthdate': player['birthday_date'],
                'position': player['role'],
                'tshirt_number': player['number_on_tshirt'],
                'is_active': True
            }
        )
        if not created:
            team_player.photo = player['player_logo']
            team_player.birthdate = player['birthday_date']
            team_player.position = player['role']
            team_player.tshirt_number = player['number_on_tshirt']
            team_player.save()

    return redirect('/home')


@login_required
@sync_to_async
def populate_coaches(request):
    if not is_admin(request.user):
        return redirect('/home')

    coaches = asyncio.run(get_coach_name())
    for coach in coaches:
        team_coach, created = Representatives.objects.get_or_create(
            name=coach['couch_name'],
            defaults={
                'photo': coach['coach_logo'],
                'birthdate': coach['birthday'],
                'role': 'Представитель'
            }
        )
        if not created:
            team_coach.photo = coach['coach_logo']
            team_coach.birthdate = coach['birthday']
            team_coach.role = 'Представитель'
            team_coach.save()

    return redirect('/home')


@login_required
def populate_old_matches(request):
    if not is_admin(request.user):
        return redirect('/home')
    matches = get_matches(played='played', sort='timeasc')
    for match in matches:
        match_record, created = Matches.objects.get_or_create(
            date=match['date'],
            time=match['time'],
            defaults={
                'tournament': match.get('tournament', ''),
                'opponent': match.get('opponent', ''),
                'stadium': match.get('stadium', ''),
                'logo1': match.get('logo1', ''),
                'stats': match.get('score', '')
            }
        )
        if not created:
            match_record.tournament = match.get('tournament', '')
            match_record.opponent = match.get('opponent', '')
            match_record.stadium = match.get('stadium', '')
            match_record.logo1 = match.get('logo1', '')
            match_record.stats = match.get('score', '')
            match_record.save()
    return redirect('/home')


@login_required
def populate_matches(request):
    if not is_admin(request.user):
        return redirect('/home')

    matches = get_matches()
    for match in matches:
        match_record, created = Matches.objects.get_or_create(
            date=match['date'],
            time=match['time'],
            defaults={
                'tournament': match.get('tournament', ''),
                'opponent': match.get('opponent', ''),
                'stadium': match.get('stadium', ''),
                'logo1': match.get('logo1', ''),
                'link': match.get('video', ''),
                'stats': match.get('score', '')
            }
        )
        if not created:
            match_record.tournament = match.get('tournament', '')
            match_record.opponent = match.get('opponent', '')
            match_record.stadium = match.get('stadium', '')
            match_record.logo1 = match.get('logo1', '')
            match_record.link = match.get('video', '')
            match_record.stats = match.get('score', '')
            match_record.save()
    return redirect('/home')


@login_required
def populate_next_matches(request):
    if not is_admin(request.user):
        return redirect('/home')
    matches = get_matches(played='notplayed', sort='timeasc')
    NextMatches.objects.all().delete()
    for match in matches:
        match_record, created = NextMatches.objects.get_or_create(
            date=match['date'],
            time=match['time'],
            defaults={
                'tournament': match.get('tournament', ''),
                'opponent': match.get('opponent', ''),
                'stadium': match.get('stadium', ''),
                'logo1': match.get('logo1', ''),
                'link': match.get('video', ''),
                'stats': match.get('score', '')
            }
        )
        if not created:
            match_record.tournament = match.get('tournament', '')
            match_record.opponent = match.get('opponent', '')
            match_record.stadium = match.get('stadium', '')
            match_record.logo1 = match.get('logo1', '')
            match_record.link = match.get('video', '')
            match_record.stats = match.get('score', '')
            match_record.save()
    return redirect('/home')
