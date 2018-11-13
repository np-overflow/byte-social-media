from django.urls import path

from . import views

urlpatterns = [
    path("", views.home),
    path("manage/", views.admin),
    path("manage/create", views.admin_input, name="admin-create"),
]