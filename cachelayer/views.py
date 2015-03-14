from django.shortcuts import render

def robots(request):
    return render(request, 'robots.txt')