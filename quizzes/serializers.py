from rest_framework import serializers
from quizzes.models import Deck, Flashcard


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = '__all__'


class DeckDetailSerializer(serializers.ModelSerializer):
    flashcards_count = serializers.SerializerMethodField()
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Deck
        fields = ['owner', 'subject', 'name', 'description', 'flashcards_count', 'total_votes']

    def get_flashcards_count(self, deck):
        return deck.flashcard_set.count()  # 해당 deck에 속하는 flashcards 개수

    def get_total_votes(self, deck):
        flashcards = deck.flashcard_set.all()
        total_votes = sum([flashcard.vote for flashcard in flashcards])  # 해당 deck에 속하는 flashcards의 vote 총합
        return total_votes


class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = '__all__'