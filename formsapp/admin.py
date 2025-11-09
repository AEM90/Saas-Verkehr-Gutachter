from django.contrib import admin
from .models import Messmethode, FieldDefinition, FormSubmission, FieldValue

class FieldDefinitionInline(admin.TabularInline):
    model = FieldDefinition
    extra = 0

@admin.register(Messmethode)
class MessmethodeAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "slug")
    inlines = [FieldDefinitionInline]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "messmethode", "company", "created_by", "created_at", "submitted")
    readonly_fields = ("created_at", "updated_at")