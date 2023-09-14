from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.UserView.as_view(), name="user_view"),
]
