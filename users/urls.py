from django.urls import path
from .views import *

urlpatterns = [
    path("", user_view, name="user_view"),
    path("create/", create_purchase, name="create_purchase"),
    path("delete/<int:pk>", delete_purchase, name="delete_purchase"),
    path("cadastro/", cadastro, name="cadastro"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("delete-account/", delete_account, name="delete_account"),
    path("analises/", analises, name="analises"),
]
