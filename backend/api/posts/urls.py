from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.home),
    path("manage/", views.admin),
    path("manage/create", views.admin_input, name="admin-create"),
    path(f"telegram/{settings.token}", views.telegram_webhook),
]
