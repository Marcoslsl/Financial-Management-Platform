import pandas as pd
from django.shortcuts import render
from .models import Purchase
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
from .analysis.main import Analise, Graph
from .utils import *
from .email.email_handler import send_mail as send_email


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


def create_purchase(request: HttpRequest) -> HttpResponse:
    req = request.POST.dict()

    if req["data_of_purchase"] == "":
        req["data_of_purchase"] = date.today()
    elif not valida_data(req["data_of_purchase"]):
        return JsonResponse(
            {
                "Error": "Data Field",
                "detail": "Invalid type in field 'data_of_purchase'",
            }
        )
    else:
        req["data_of_purchase"] = transform_date(req["data_of_purchase"])

    user = User.objects.get(username=request.user)
    purchase = Purchase.objects.create(
        user=user,
        name=req["name"],
        price=float(req["price"]),
        category=req["category"],
        credit_card=req["credit_card"],
        description=req["description"],
        data_of_purchase=req["data_of_purchase"],
    )
    purchase.save()
    return redirect("user_view")


def update_purchase(request: HttpRequest, pk: int) -> HttpResponse:
    purchase = Purchase.objects.get(pk=pk)
    return render(
        request,
        "users/edit_purchase.html",
        {
            "purchase_list": purchase,
            "today_date": date.today().strftime("%d-%m-%Y"),
            "pk_value": pk,
            "data_of_purchase": transform_date_inverse(
                str(purchase.data_of_purchase)
            ),
        },
    )


def update_purchase_values(request: HttpRequest, pk: int) -> HttpResponse:
    req = request.POST.dict()
    purchase = Purchase.objects.get(pk=pk)
    purchase.update_purchase(**req)
    return redirect("user_view")


def delete_purchase(request: HttpRequest, pk: int) -> HttpResponse:
    purchase = Purchase(pk=pk)
    purchase.delete()
    return redirect("user_view")


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
    user = User.objects.get(request.user)
    user.delete()
    return redirect("login")


@login_required(login_url="login")
def analises(request: HttpRequest) -> HttpRequest:
    analise = Analise()

    purchases_list = analise.return_json_purchase_by_user(request)

    if len(purchases_list) == 0:
        return render(
            request,
            "users/analises.html",
        )

    df = pd.DataFrame(purchases_list)

    df["data_of_purchase"] = pd.to_datetime(df["data_of_purchase"])

    kwargs = {
        "x": "data_of_purchase",
        "y": "price",
        "hover_data": "name",
        "color": "credit_card",
        "trendline": "ols",
        "trendline_scope": "overall",
    }

    chart = Graph().scatter(
        df=df, title="Gastos ao longo do tempo | Tendência de gastos", **kwargs
    )
    purchases_analysis = analise.analyse_current_month_and_last_month(request)

    return render(
        request,
        "users/analises.html",
        {"chart": chart, "purchases_analysis": purchases_analysis},
    )
