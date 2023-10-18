from django.urls import path, include
from utils.rendering import *
from quizzes.views import (DeckView, DeckDetailView)
urlpatterns = [
    path('myquiz/', r_quiz, name='r_quiz'),
    path('', DeckView.as_view()),
    path('<int:deck_id>/', DeckDetailView.as_view())
]