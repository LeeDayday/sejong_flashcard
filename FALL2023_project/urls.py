"""
URL configuration for FALL2023_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import *
from utils.rendering import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # 페이지 렌더링
    path('login/', r_login),
    path('home/', r_home),
    path('home/quizzes/', include('quizzes.urls')),
    path('home/quizzes/add_deck', r_add_deck),

    # 함수 사용 렌더링
    path('f_login/', f_login, name='f_login'),
    path('f_logout/', f_logout, name='f_logout'),

    # 퀴즈 랜더링

    # 캘린더 랜더링
    ### path('home/cal', include('cal.urls')),
]