from django.core.files.base import ContentFile
from .models import GeneratedReport
from docxtpl import DocxTemplate
from django.template import Template, Context
import io
import traceback

try:
    # optional for HTML->PDF path
    from weasyprint import HTML
except Exception:
    HTML = None

def generate_report_sync(generated_report_id):
    """
    Synchronous report generation helper.
    - Loads GeneratedReport by id, renders the associated template using submission.field_values,
      writes the generated file to the GeneratedReport.file, updates status and error.
    - Raises exceptions so callers can handle/log them if needed.
    """
    gr = None
    try:
        gr = GeneratedReport.objects.select_related("template", "submission").get(pk=generated_report_id)
        template = gr.template
        submission = gr.submission

        # Build context from field values:
        context = {}
        for fv in submission.field_values.all().select_related("field"):
            key = fv.field.name if fv.field else f"field_{fv.pk}"
            # prefer value_text; for files we can reference URL or leave blank
            if fv.value_text:
                context[key] = fv.value_text
            elif fv.value_file:
                # When using docxtpl InlineImage you'd handle differently; provide URL for simple placeholders
                try:
                    context[key] = fv.value_file.url
                except Exception:
                    context[key] = ""
            else:
                context[key] = ""

        filename = (template.template_file.name or "").lower()

        if filename.endswith(".docx"):
            tpl_file = template.template_file
            # DocxTemplate accepts file path or file-like. Try filesystem path first.
            try:
                doc = DocxTemplate(tpl_file.path)
            except Exception:
                tpl_bytes = tpl_file.read()
                doc = DocxTemplate(io.BytesIO(tpl_bytes))

            doc.render(context)
            out = io.BytesIO()
            doc.save(out)
            out.seek(0)
            gr.file.save(f"report_{gr.pk}.docx", ContentFile(out.read()))
            gr.status = "done"
            gr.error = ""
            gr.save()
            return {"status": "done"}

        elif filename.endswith(".html") or filename.endswith(".htm"):
            if HTML is None:
                gr.status = "failed"
                gr.error = "WeasyPrint is not available"
                gr.save()
                return {"status": "failed", "error": gr.error}
            raw = ""
            try:
                # Template stored in storage; read bytes and decode
                raw = template.template_file.read().decode("utf-8")
            except Exception:
                try:
                    raw = template.template_file.read()
                except Exception:
                    raw = ""
            t = Template(raw)
            rendered = t.render(Context(context))
            pdf = HTML(string=rendered).write_pdf()
            gr.file.save(f"report_{gr.pk}.pdf", ContentFile(pdf))
            gr.status = "done"
            gr.error = ""
            gr.save()
            return {"status": "done"}

        else:
            gr.status = "failed"
            gr.error = "Unsupported template type"
            gr.save()
            return {"status": "failed", "error": gr.error}

    except Exception as e:
        tb = traceback.format_exc()
        if gr:
            try:
                gr.status = "failed"
                gr.error = str(e) + "\n" + tb
                gr.save()
            except Exception:
                pass
        # Re-raise so callers (views) can catch and show messages/log
        raise