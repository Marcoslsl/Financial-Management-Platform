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
    purchase = Purchase.objects.all()
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

    purchase = Purchase(
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
