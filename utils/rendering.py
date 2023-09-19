from django.shortcuts import render


def r_login(request):
    response = render(request, "login_page/loginPage.html")
    return response

def r_home(request):
    response = render(request, "main_page/main_page.html")
    return response

