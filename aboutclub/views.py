from django.shortcuts import render


def about_club_page(request):
    return render(request, 'aboutclub.html')
