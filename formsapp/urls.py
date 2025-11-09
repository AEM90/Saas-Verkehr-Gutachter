from django.urls import path
from . import views

app_name = "formsapp"

urlpatterns = [
    path("m/<slug:slug>/", views.messmethode_detail, name="messmethode_detail"),
    path("submission/<int:pk>/", views.submission_detail, name="submission_detail"),
]