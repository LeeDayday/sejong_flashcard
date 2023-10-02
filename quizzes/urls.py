from django.urls import path, include
from utils.rendering import *

urlpatterns = [
    path('myquiz/', r_quiz, name = 'r_quiz')
]