from django.urls import path
from .views import *

urlpatterns = [
    path("", user_view, name="user_view"),
    path("create/", create_purchase, name="create_purchase"),
    path("delete/<int:pk>", delete_purchase, name="delete_purchase"),
    path("update/<int:pk>", update_purchase, name="update_purchase"),
    path(
        "update_send_form/<int:pk>",
        update_purchase_values,
        name="update_purchase_values",
    ),
    path("cadastro/", cadastro, name="cadastro"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("delete-account/", delete_account, name="delete_account"),
    path("analises/", analises, name="analises"),
    path(
        "send-reminding-email-to-all-users/",
        send_mail_to_all_users,
        name="email",
    ),
]
