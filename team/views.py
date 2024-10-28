from asgiref.sync import sync_to_async
from django.shortcuts import render
from main.models import Team, Representatives


@sync_to_async
def team(request):
    type = request.GET.get('type')
    if not type:
        type = 'active'
    if type == 'active':
        team = Team.objects.all()
        context = {'team': team, 'type': type}
        return render(request, 'team/team.html', context)
    if type == 'inactive':
        team = Team.objects.all()
        context = {'team': team, 'type': type}
        return render(request, 'team/team.html', context)
    if type == 'representatives':
        team = Representatives.objects.all()
        context = {'team': team, 'type': type}
        return render(request, 'team/team.html', context)


def player_info(request):
    id = request.GET.get('id')
    player = Team.objects.get(id=id)
    attrs = {
        'player' : player
    }
    return render(request, 'team/player_info.html', attrs)