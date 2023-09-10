from django.shortcuts import render


def r_login(request):
    response = render(request, "login_page/loginPage.html")
    return response
