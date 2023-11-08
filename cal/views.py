from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from utils.permission import IsOwnerOrReadOnly
from .models import *
from cal.serializers import CalenderSerializer, ContentSerializer

# Create your views here.

class CalendarView(APIView, PageNumberPagination):

    "Calendar 조회"
    def get(self, request):
        all_cal = Calendar.objects.all()
        page = self.paginate_queryset(all_cal, request)
        serializer = CalenderSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    "Calendar 생성"
    def post(self, request):
        info = request.data
        info['owner'] = request.user.student_id
        serializer = CalenderSerializer(data = info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CalendarDetailView(APIView, PageNumberPagination):

    "Calendar 상세조회"

    def get(self, request, calendar_id):
        cal = get_object_or_404(Calendar, id = calendar_id)
        serializer = CalenderSerializer(cal)
        return Response(serializer.data)

    "Calendar 수정"
    def put(self, request, calendar_id):
        cal = get_object_or_404(Calendar, id=calendar_id)
        serializer = CalenderSerializer(cal, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    "Calendar 삭제"
    def delete(self, request, calendar_id):
        cal = get_object_or_404(Calendar, id=calendar_id)
        cal.delete()
        return Response("삭제 되었습니다.", status=HTTP_204_NO_CONTENT)



class ContentView(APIView, PageNumberPagination):
    permission_classes = [IsOwnerOrReadOnly]

    "Cal에 대한 Content 조회"
    def get(self, request, calendar_id):
        cal = get_object_or_404(Calendar, id = calendar_id)
        all_contents = cal.content_set.all()
        page = self.paginate_queryset(all_contents, request)
        serializer = ContentSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


    "Cal에 대한 Content 생성"
    def post(self, request, calendar_id):
        info = request.data
        info['owner'] = request.user.student_id
        info['calendar'] = calendar_id
        serializer = ContentSerializer(data = info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)

class ContentDetailView(APIView, PageNumberPagination):
    permission_classes = [IsOwnerOrReadOnly]

    "Content 상세 조회"
    def get(self, request, calendar_id, content_id):
        content = get_object_or_404(Content, id = content_id)
        serializer = ContentSerializer(content)
        return Response(serializer.data)

    "수정"
    def put(self, request, calendar_id, content_id):
        content = get_object_or_404(Content, id = content_id)
        serializer = ContentSerializer(content, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    "삭제"
    def delete(self, request, calendar_id, content_id):
        content = get_object_or_404(Content, id = content_id)
        content.delete()
        return Response("삭제되었습니다", status = HTTP_204_NO_CONTENT)
