from django.contrib import admin
from .models import ReportTemplate, GeneratedReport

@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "messmethode", "created_at")

@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = ("id", "submission", "template", "status", "created_at")
    readonly_fields = ("created_at", "error")