from django.urls import path, include
from utils.rendering import *
from quizzes.views import (DeckView, DeckDetailView, FlashcardView, FlashcardDetailView)
urlpatterns = [
    path('myquiz/', r_quiz, name='r_quiz'),
    path('', DeckView.as_view()),
    path('<int:deck_id>/', DeckDetailView.as_view()),
    path('<int:deck_id>/cards/', FlashcardView.as_view()),
    path('<int:deck_id>/cards/<int:flashcard_id>', FlashcardDetailView.as_view()),
]