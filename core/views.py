from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from formsapp.models import FormSubmission, Messmethode

@login_required
def landing(request):
    """
    Landing page for logged-in users: links to History, Create Report and Admin.
    """
    return render(request, "core/landing.html", {})

@login_required
def history(request):
    """
    List submissions for the current user's company (most recent first).
    """
    company = getattr(request.user, "company", None)
    submissions = FormSubmission.objects.none()
    if company:
        submissions = FormSubmission.objects.filter(company=company).order_by("-created_at")
    return render(request, "core/history.html", {"submissions": submissions})

@login_required
def create_report(request):
    """
    Show available Messmethodes (forms) for the company so the user can open a form and create reports.
    """
    company = getattr(request.user, "company", None)
    messmethodes = Messmethode.objects.none()
    if company:
        messmethodes = Messmethode.objects.filter(company=company).order_by("name")
    return render(request, "core/create_report.html", {"messmethodes": messmethodes})