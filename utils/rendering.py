from django.shortcuts import render


def r_login(request):
    response = render(request, "login.html")
    return response


def r_home(request):
    response = render(request, "main.html")
    return response


def r_myquiz(request):
    response = render(request, "myQuiz.html")
    return response


def r_newquiz(request):
    response = render(request, "add_quiz(deck).html")
    return response

def r_solvequiz(request):
    response = render(request, "attempt_quiz.html")
    return response
