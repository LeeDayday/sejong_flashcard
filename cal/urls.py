from django.urls import path, include
from .views import *
from utils.rendering import *

app_name = 'cal'
urlpatterns = [
    # path("", CalendarView.as_view()),
    # path("<int:calendar_id>/", CalendarDetailView.as_view()),
    path("<int:calendar_id>/contents/", ContentView.as_view(), name="content"),
    path("<int:calendar_id>/contents/<int:content_id>/", ContentDetailView.as_view()),
    path("mycal/", CalendarView2.as_view(), name='calendar'),
    path("mycal/content/new/", login_required(content), name = "content_new"),
    path("mycal/content/edit/<int:content_id>/", login_required(content), name = "content_edit"),
    # path("mycal/content/delete/<int:content_id>/", content_delete, name="content_delete"),

    path('contest/', r_contest, name='r_contest'),

]