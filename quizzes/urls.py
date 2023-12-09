from django.urls import path, include
from utils.rendering import *
from quizzes.views import (DeckView, DeckDetailView, FlashcardView, FlashcardDetailView,
                           FlashcardAttemptView, VoteFlashcardView, MyDeckView)

app_name = 'quizzes'

urlpatterns = [
    path('', DeckView.as_view(), name='deck-list'),
    path('myquiz/', MyDeckView.as_view(), name='my-quiz'),
    path('<int:deck_id>/', DeckDetailView.as_view(), name='deck-detail'),
    path('<int:deck_id>/delete/', DeckDetailView.as_view(), name='deck-delete'), #삭제하기 url
    path('<int:deck_id>/cards/', FlashcardView.as_view(), name='card-list'),
    path('<int:deck_id>/cards/<int:flashcard_id>', FlashcardDetailView.as_view(), name='card-detail'),
    path('<int:deck_id>/cards/<int:flashcard_id>/delete/', FlashcardDetailView.as_view(), name='card-delete'),
    path('<int:deck_id>/cards/attempt/<int:flashcard_id>', FlashcardAttemptView.as_view(), name='card-attempt'),
    path('<int:deck_id>/cards/<int:flashcard_id>/vote/', VoteFlashcardView.as_view(), name='vote_flashcard'),

]