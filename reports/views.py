from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from .models import GeneratedReport, ReportTemplate
from django.template import Template, Context
from django.utils.encoding import smart_str
import traceback

try:
    from weasyprint import HTML
except Exception:
    HTML = None

def report_status(request, pk):
    """
    Returns JSON status for GeneratedReport with id=pk.
    { status: "pending"|"done"|"failed", download_url: "/media/..." }
    """
    gr = get_object_or_404(GeneratedReport, pk=pk)
    data = {"status": gr.status or "pending", "download_url": ""}
    try:
        if gr.file and hasattr(gr.file, "url"):
            data["download_url"] = gr.file.url
    except Exception:
        data["download_url"] = ""
    return JsonResponse(data)


def report_preview(request, template_id):
    """
    Render a preview for a ReportTemplate (HTML). If WeasyPrint available, return PDF.
    - Only supports HTML templates for preview; DOCX previews are not generated here.
    """
    rt = get_object_or_404(ReportTemplate, pk=template_id)
    filename = (rt.template_file.name or "").lower()
    # Build a simple sample context
    context = {
        "company_name": getattr(rt.company, "name", "Company"),
        "template": rt,
        "submission": type("S", (), {"pk": "preview", "created_at": "", "messmethode": rt.messmethode, "field_values": []})(),
    }

    # If HTML template:
    if filename.endswith(".html") or filename.endswith(".htm"):
        try:
            raw = rt.template_file.read().decode("utf-8")
        except Exception:
            # try reading bytes and decode
            try:
                raw = smart_str(rt.template_file.read())
            except Exception:
                raw = ""
        try:
            t = Template(raw)
            rendered = t.render(Context(context))
        except Exception as e:
            tb = traceback.format_exc()
            return HttpResponseBadRequest(f"Template rendering error: {e}\n\n{tb}", content_type="text/plain")

        # If weasyprint available, return PDF
        if HTML is not None:
            try:
                pdf = HTML(string=rendered).write_pdf()
                resp = HttpResponse(pdf, content_type="application/pdf")
                resp["Content-Disposition"] = 'inline; filename="preview.pdf"'
                return resp
            except Exception as e:
                # fallback to HTML
                return HttpResponse(rendered, content_type="text/html")
        else:
            # Return HTML if no PDF engine
            return HttpResponse(rendered, content_type="text/html")

    else:
        return HttpResponseBadRequest("Preview only supported for HTML templates. For DOCX use the DOCX generation flow.", content_type="text/plain")