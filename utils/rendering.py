from django.shortcuts import render


def r_login(request):
    response = render(request, "login.html")
    return response


def r_home(request):
    response = render(request, "main.html")
    return response


def r_quiz(request):
    response = render(request, "myQuiz.html")
    return response
