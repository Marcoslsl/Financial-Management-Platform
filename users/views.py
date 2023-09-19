import pandas as pd
import plotly.express as px
from django.shortcuts import render
from .models import Purchase
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import redirect
from datetime import date, datetime
import re
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login as login_django,
    logout as logout_django,
)
from django.contrib.auth.decorators import login_required
from .analysis.main import Analise


def valida_data(data: str) -> bool:
    padrao = r"^\d{2}[-/]\d{2}[-/]\d{4}$"

    if re.match(padrao, data):
        return True
    else:
        return False


def transform_date(input_date: str) -> str:
    date_obj = datetime.strptime(input_date, "%d-%m-%Y")

    output_date = date_obj.strftime("%Y-%m-%d")

    return output_date


@login_required(login_url="login")
def user_view(request):
    username = request.user
    purchase = Purchase.objects.filter(user=username)
    return render(
        request, "users/purchase_list.html", {"purchase_list": purchase}
    )


def create_purchase(request: HttpRequest) -> any:
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


def delete_purchase(request: HttpRequest, pk: int) -> any:
    purchase = Purchase(pk=pk)
    purchase.delete()
    return redirect("user_view")


def cadastro(request):
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


def login(request):
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
            return JsonResponse({"Error": "Unauthorized"})


def logout(request):
    logout_django(request)
    return redirect("login")


def delete_account(request):
    user = User.objects.get(request.user)
    user.delete()
    return redirect("login")


@login_required(login_url="login")
def analises(request):
    analise = Analise()

    purchases_list = analise.return_json_purchase_by_user(request)

    if len(purchases_list) == 0:
        return render(
            request,
            "users/analises.html",
        )

    df = pd.DataFrame(purchases_list)

    df["data_of_purchase"] = pd.to_datetime(df["data_of_purchase"])

    fig = px.scatter(
        df,
        x="data_of_purchase",
        y="price",
        hover_data="name",
        color="credit_card",
        trendline="ols",
        trendline_scope="overall",
    )

    fig.update_layout(
        title_text="Gastos ao longo do tempo | Tendência de gastos",
        title_x=0.45,  # Define o título no meio horizontal do gráfico (0 a 1)
        title_font=dict(size=30, family="Arial, sans-serif", color="black"),
    )

    fig.update_layout(height=700)
    chart = fig.to_html()

    purchases_analysis = analise.analyse_current_month_and_last_month(request)
    return render(
        request,
        "users/analises.html",
        {"chart": chart, "purchases_analysis": purchases_analysis},
    )
