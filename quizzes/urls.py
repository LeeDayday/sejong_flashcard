from django.urls import path, include
from utils.rendering import *
from quizzes.views import (DeckView)
urlpatterns = [
    path('myquiz/', r_quiz, name='r_quiz'),
    path('', DeckView.as_view())
]