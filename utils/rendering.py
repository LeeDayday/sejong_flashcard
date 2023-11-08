from django.shortcuts import render, redirect
from django.contrib import messages

def r_login(request):
    response = render(request, "login.html")
    return response


def r_home(request):
    response = render(request, "main.html")
    return response


def r_quiz(request):
    response = render(request, "add_quiz(deck).html")
    return response

def r_add_deck(request):
    response = render(request, "add_quiz(deck).html")
    return response