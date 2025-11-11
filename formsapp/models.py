from django.db import models
from django.conf import settings

class Messmethode(models.Model):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="messmethodes")
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("company", "slug")

    def __str__(self):
        return f"{self.company} - {self.name}"

FIELD_TYPES = [
    ("text", "Text"),
    ("number", "Number"),
    ("date", "Date"),
    ("choice", "Choice"),
    ("file", "File"),
    ("boolean", "Boolean"),
]

class FieldDefinition(models.Model):
    messmethode = models.ForeignKey(Messmethode, related_name="fields", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # internal field key
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    meta = models.JSONField(default=dict, blank=True)  # choices, validation, page, etc.

    class Meta:
        ordering = ["order"]
        unique_together = ("messmethode", "name")

    def __str__(self):
        return f"{self.messmethode.name}: {self.label}"

class FormSubmission(models.Model):
    messmethode = models.ForeignKey(Messmethode, on_delete=models.PROTECT)
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.messmethode.name} submission #{self.pk}"

class FieldValue(models.Model):
    submission = models.ForeignKey(FormSubmission, related_name="field_values", on_delete=models.CASCADE)
    field = models.ForeignKey(FieldDefinition, on_delete=models.SET_NULL, null=True)
    value_text = models.TextField(blank=True, null=True)
    value_file = models.FileField(upload_to="submission_files/", blank=True, null=True)

    def __str__(self):
        return f"val {self.field} -> {self.submission}"