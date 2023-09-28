from django.urls import path
from .views import *

urlpatterns = [
    path("", user_view, name="user_view"),
    path("cadastro/", cadastro, name="cadastro"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("delete-account/", delete_account, name="delete_account"),
    path(
        "send-reminding-email-to-all-users/",
        send_mail_to_all_users,
        name="email",
    ),
]
