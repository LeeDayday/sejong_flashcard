from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Deck
from .serializers import DeckSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


class DeckView(APIView, PageNumberPagination):
    """
    Deck 리스트 조회
    """
    def get(self, request):
        all_decks = Deck.objects.all()
        page = self.paginate_queryset(all_decks, request)
        serializer = DeckSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    """
    Deck 생성
    """
    def post(self, request):
        data = request.data
        data['owner'] = request.user.student_id
        serializer = DeckSerializer(data=data)
        if serializer.is_valid():
            serializer.save() # owner field를 채운 새로운 모델 인스턴스 생성 및 저장
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)








