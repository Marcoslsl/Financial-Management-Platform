from django.shortcuts import render
from .models import Purchase
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import redirect
from datetime import date, datetime
import re


def valida_data(data: str) -> bool:
    padrao = r"^\d{2}-\d{2}-\d{4}$"

    if re.match(padrao, data):
        return True
    else:
        return False


def transform_date(input_date: str) -> str:
    date_obj = datetime.strptime(input_date, "%d-%m-%Y")

    output_date = date_obj.strftime("%Y-%m-%d")

    return output_date


class UserView(ListView):
    model = Purchase


def create_purchase(request: HttpRequest) -> any:
    req = request.POST.dict()

    print(date.today())
    print(req["data_of_purchase"])

    if req["data_of_purchase"] == "":
        req["data_of_purchase"] = date.today()
    elif not valida_data(req["data_of_purchase"]):
        return JsonResponse(
            {"Error": "Invalid type in field 'data_of_purchase'"}
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


# class CreatePurchase(CreateView):
#     model = Purchase
#     fields = [
#         "name",
#         "price",
#         "category",
#         "credit_card",
#         "description",
#         "data_of_purchase",
#     ]
#     success_url = reverse_lazy("user_view")
