from django.urls import path
from .views import *

urlpatterns = [
    path("create/", create_purchase, name="create_purchase"),
    path("delete/<int:pk>", delete_purchase, name="delete_purchase"),
    path("update/<int:pk>", update_purchase, name="update_purchase"),
    path(
        "update_send_form/<int:pk>",
        update_purchase_values,
        name="update_purchase_values",
    ),
    path("analises/", analises, name="analises"),
]
