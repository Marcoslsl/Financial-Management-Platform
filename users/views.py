from django.shortcuts import render
from .models import Purchase
from django.views.generic import (
    ListView,
)


class UserView(ListView):
    model = Purchase
