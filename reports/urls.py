from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("<int:pk>/status/", views.report_status, name="report_status"),
    path("preview/<int:template_id>/", views.report_preview, name="report_preview"),
]