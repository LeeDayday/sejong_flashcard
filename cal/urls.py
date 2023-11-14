from django.urls import path, include
from .views import *
from utils.rendering import *

urlpatterns = [
    path("", CalendarView.as_view()),
    path("<int:calendar_id>/", CalendarDetailView.as_view()),
    path("<int:calendar_id>/contents/", ContentView.as_view(), name="content"),
    path("<int:calendar_id>/contents/<int:content_id>/", ContentDetailView.as_view()),
    path("mycal/", CalendarView2.as_view(), name='calendar'),
]