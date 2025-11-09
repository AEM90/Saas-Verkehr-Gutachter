from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Messmethode, FormSubmission, FieldValue
from reports.models import GeneratedReport, ReportTemplate
# Use the synchronous helper
from reports.utils import generate_report_sync
from .forms import build_form_for_messmethode

@login_required
def messmethode_detail(request, slug):
    """
    Display a Messmethode form (built from FieldDefinition). Handles saving a draft submission
    and optionally creating a GeneratedReport and generating the report synchronously.
    """
    mm = get_object_or_404(Messmethode, slug=slug, company=request.user.company)

    # Build form from FieldDefinitions
    form = build_form_for_messmethode(mm, data=request.POST or None, files=request.FILES or None)

    if request.method == "POST" and form.is_valid():
        # create a FormSubmission (draft) or update an existing one if provided
        submission_id = request.POST.get("submission_id")
        if submission_id:
            submission = get_object_or_404(FormSubmission, pk=int(submission_id), company=request.user.company)
            submission.submitted = request.POST.get("submitted", "false") == "true"
            submission.save()
        else:
            submission = FormSubmission.objects.create(
                messmethode=mm,
                company=request.user.company,
                created_by=request.user,
                submitted=request.POST.get("submitted", "false") == "true",
            )

        # Save each field value. For file fields, check request.FILES
        for fd in mm.fields.all():
            key = fd.name
            # delete existing value for this field/submission (simple overwrite)
            FieldValue.objects.filter(submission=submission, field=fd).delete()
            if fd.field_type == "file":
                uploaded = request.FILES.get(key)
                if uploaded:
                    fv = FieldValue.objects.create(submission=submission, field=fd, value_file=uploaded)
            else:
                val = form.cleaned_data.get(key)
                if val is not None:
                    # store everything as text for now
                    FieldValue.objects.create(submission=submission, field=fd, value_text=str(val))

        # If user clicked "generate", create GeneratedReport and generate synchronously
        if "generate" in request.POST:
            # pick a template for this messmethode - use first available or let admin choose in UI later
            template = ReportTemplate.objects.filter(company=request.user.company, messmethode=mm).first()
            if not template:
                messages.error(request, "No report template found for this Messmethode. Please ask an admin to upload one.")
                return redirect(reverse("formsapp:submission_detail", args=[submission.pk]))

            gr = GeneratedReport.objects.create(submission=submission, template=template, status="pending")
            try:
                # Synchronous generation (blocks the request until finished)
                generate_report_sync(gr.id)
                messages.success(request, "Report generated. You can download it from the submission page.")
            except Exception as e:
                # generate_report_sync already sets gr.status to 'failed' and records the error where possible
                messages.error(request, f"Report generation failed: {e}")
            return redirect(reverse("formsapp:submission_detail", args=[submission.pk]))

        messages.success(request, "Form saved.")
        return redirect(reverse("formsapp:submission_detail", args=[submission.pk]))

    # GET: show form. Optionally pass submission id to prepopulate fields (not implemented here)
    context = {
        "messmethode": mm,
        "form": form,
    }
    return render(request, "formsapp/messmethode_detail.html", context)

@login_required
def submission_detail(request, pk):
    submission = get_object_or_404(FormSubmission, pk=pk, company=request.user.company)
    field_values = submission.field_values.select_related("field").all()
    reports = submission.reports.all().order_by("-created_at")
    return render(request, "formsapp/submission_detail.html", {"submission": submission, "field_values": field_values, "reports": reports})