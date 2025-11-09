from django.db import models

class ReportTemplate(models.Model):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE)
    messmethode = models.ForeignKey("formsapp.Messmethode", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    template_file = models.FileField(upload_to="report_templates/")  # .docx or .html
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.name}"

class GeneratedReport(models.Model):
    submission = models.ForeignKey("formsapp.FormSubmission", on_delete=models.CASCADE, related_name="reports")
    template = models.ForeignKey(ReportTemplate, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to="generated_reports/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("pending","pending"),("done","done"),("failed","failed")], default="pending")
    error = models.TextField(blank=True)

    def __str__(self):
        return f"Report {self.pk} for submission {self.submission_id}"