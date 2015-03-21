from django.shortcuts import render


def robots(request):
    return render(request, 'robots.txt')


def angular_app(request):
    return render(request, 'angular_app.html')
