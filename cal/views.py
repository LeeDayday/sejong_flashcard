from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.views import APIView
# from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from utils.permission import IsOwnerOrReadOnly
from .models import *
from cal.serializers import *
from django.shortcuts import get_object_or_404, redirect
import calendar
from django.urls import reverse
from django.shortcuts import render
from .utils import Calendar2
from django.utils.safestring import mark_safe
from django.views import generic
from datetime import datetime, timedelta, date
from .forms import ContentForm
from django.contrib import messages


# Create your views here.
# class CalendarView(APIView, PageNumberPagination):
#
#     "Calendar 조회"
#     def get(self, request):
#         all_cal = Calendar.objects.all()
#         page = self.paginate_queryset(all_cal, request)
#         serializer = CalenderSerializer(page, many=True)
#         return self.get_paginated_response(serializer.data)
#
#     "Calendar 생성"
#     def post(self, request):
#         info = request.data
#         info['owner'] = request.user.student_id
#         serializer = CalenderSerializer(data = info)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=HTTP_201_CREATED)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
#
#
# class CalendarDetailView(APIView, PageNumberPagination):
#
#     "Calendar 상세조회"
#
#     def get(self, request, calendar_id):
#         cal = get_object_or_404(Calendar, id = calendar_id)
#         serializer = CalenderSerializer(cal)
#         return Response(serializer.data)
#
#     "Calendar 수정"
#     def put(self, request, calendar_id):
#         cal = get_object_or_404(Calendar, id=calendar_id)
#         serializer = CalenderSerializer(cal, data = request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
#
#     "Calendar 삭제"
#     def delete(self, request, calendar_id):
#         cal = get_object_or_404(Calendar, id=calendar_id)
#         cal.delete()
#         return Response("삭제 되었습니다.", status=HTTP_204_NO_CONTENT)



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

class CalendarView2(generic.ListView):
    model = Content
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar2(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    try:
        if req_day:
            year, month, day = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
    except (ValueError, TypeError):
        pass
    return datetime.today().date()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    a = 'day=' + str(prev_month.year) + '-' + str(prev_month.month) + '-' + str(prev_month.day)
    return a


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    a = 'day=' + str(next_month.year) + '-' + str(next_month.month) + '-' + str(next_month.day)
    return a


@login_required
def content(request, content_id=None):
    instance = Content()
    if content_id:
        instance = get_object_or_404(Content, pk=content_id)
    else:
        instance = Content()
    form = ContentForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/content.html', {'form': form, 'instance':instance})


def content_delete(request, content_id=None):
    instance = Content()
    if content_id:
        instance = get_object_or_404(Content, pk=content_id)
    else:
        instance = Content()
    if request.method == 'POST':
        instance.delete()
        messages.success(request, '성공적으로 삭제하였습니다.')
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/delete.html', {'instance': instance})

