from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Deck
from .serializers import DeckSerializer


class DeckView(APIView, PageNumberPagination):
    """
    Deck 리스트 조회
    """
    def get(self, request):
        all_decks = Deck.objects.all()
        page = self.paginate_queryset(all_decks, request)
        serializer = DeckSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)







