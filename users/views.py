import pandas as pd
from django.shortcuts import render
from purchases.models import Purchase
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import redirect
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login as login_django,
    logout as logout_django,
)
from django.contrib.auth.decorators import login_required
from utils import *
from .email.email_handler import send_mail as send_email
from django.shortcuts import get_object_or_404


def send_mail_to_all_users(request: HttpRequest) -> JsonResponse:
    subject = "Lembrete | Plataforma de gerenciamento financeiro"
    message = "Lembre de adicionar os dados de gastos dessa semana. https://django-financial-management-platform.onrender.com/"
    emails_to_send = User.objects.filter(is_superuser=False)
    emails = list(set([email.email for email in emails_to_send]))

    res = send_email(
        request,
        subject,
        message,
        emails,
    )

    return JsonResponse(res)


@login_required(login_url="login")
def user_view(request: HttpRequest) -> HttpResponse:
    username = request.user
    purchase = Purchase.objects.filter(user=username)
    return render(
        request,
        "users/purchase_list.html",
        {
            "purchase_list": purchase,
            "today_date": date.today().strftime("%d-%m-%Y"),
        },
    )


def cadastro(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "users/cadastro.html")
    else:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(username=username).first()
        if user:
            return JsonResponse({"Error": "User already registed"})

        new_user = User.objects.create_user(
            username=username, email=email, password=password
        )
        new_user.save()
        return redirect("user_view")


def login(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "users/login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login_django(request, user)
            return redirect("user_view")
        else:
            return HttpResponse({"Error": "Unauthorized"})


def logout(request: HttpRequest) -> HttpResponse:
    logout_django(request)
    return redirect("login")


def delete_account(request: HttpRequest) -> HttpResponse:
    user = get_object_or_404(User, username=request.user)
    user.delete()
    return redirect("login")
