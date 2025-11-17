"""URL patterns for the `accounts` app (admin-protected user management)."""

from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("users/", views.users_list, name="users_list"),
    path("users/add/", views.user_add, name="user_add"),
    path("users/<int:user_id>/edit/", views.user_edit, name="user_edit"),
]
