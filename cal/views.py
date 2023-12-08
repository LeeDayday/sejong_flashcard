from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from utils.permission import IsOwnerOrReadOnly
from cal.serializers import *
from django.shortcuts import get_object_or_404, redirect
import calendar
from django.urls import reverse
from django.shortcuts import render
from .utils import *
from django.utils.safestring import mark_safe
from django.views import generic
from datetime import datetime, timedelta, date
from .forms import ContentForm
from django.contrib import messages
from .models import NewUserInfo
from .data import contest_data_list


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
    permission_classes = [IsOwnerOrReadOnly]
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


def content(request, content_id=None):
    owner = NewUserInfo.objects.latest('updated_at')
    instance = Content()
    if content_id:
        instance = get_object_or_404(Content, pk=content_id, owner=owner)
    else:
        instance = Content(owner=owner)
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


def contest_data(request):
    data = contest_data_list()
    return render(request, 'cal/contest_data.html', {'data': data})


def save_contest_data(request):
    owner = NewUserInfo.objects.latest('updated_at')
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        date_ = request.POST.get('date')
        y,m,d = map(int, str(date_).split('-'))
        Content(owner = owner,
                title = title,
                content = content,
                start_time = date(y,m,d),
                end_time = date(y,m,d)).save()
        return HttpResponseRedirect(reverse('cal:contest_data'))
    return render(request, 'cal/contest_data.html')


def school_cal_data(request):
    data = school_cal_crawling()
    return render(request, 'cal/school_cal_data.html', {'data': data})


def save_school_cal_data(request):
    owner = NewUserInfo.objects.latest('updated_at')
    if request.method == "POST":
        content = request.POST.get('content')
        date = request.POST.get('date')
        year, month = map(int, date.split('/'))

        if content[0].isdigit() and content[1].isdigit():
            x = check(content, 5)
        else:
            x = check(content, 4)

        info = content[x:]
        tmp = content[:x]
        day, st = [], ""
        for k in tmp:
            if k.isdigit():
                st += k
            else:
                if st: day.append(int(st))
                st = ""
        if len(day) == 3:
            m = check_month(month)
            for d in range(day[0], m + 1):
                save_content(owner, info, info, year, month, d)
            if day[1] < month:
                k = 1
            else:
                k = 0
            for d in range(1, day[2] + 1):
                save_content(owner, info, info, year + k, day[1], d)
        elif len(day) == 2:
            for d in range(day[0], day[1] + 1):
                save_content(owner, info, info, year, month, d)
        else:
            save_content(owner, info, info, year, month, day[0])
        return HttpResponseRedirect(reverse('cal:school_cal_data'))

    return render(request, 'cal/school_cal_data.html')


def check(j, t):
    tmp = j[t:]
    if tmp[0] == ')':
        t += 1
        tmp = j[t:]
    print(tmp)
    if ')' in tmp:
        x = j[t:].index(')') + t+1
        print(x)
        z = 14 if t == 5 else 13
        if x > z:
            x = t
    else:
        x = t
    return x

def check_month(x):
    m30 = [4, 6, 9, 11]
    if x == 2:return 28
    elif x in m30:return 30
    else:
        return 31

def save_content(owner, title, content, y,m,d):
    Content(owner=owner,
            title=title,
            content=content,
            start_time=date(y, m, d),
            end_time=date(y, m, d)).save()
