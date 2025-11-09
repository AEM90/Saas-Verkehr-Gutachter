from django import forms
from .models import FieldDefinition
from django.utils import timezone

FIELD_WIDGETS = {
    "text": forms.TextInput,
    "number": forms.NumberInput,
    "date": forms.DateInput,
    "choice": forms.Select,
    "file": forms.ClearableFileInput,
}

def build_form_for_messmethode(messmethode, data=None, files=None):
    """
    Dynamically build a Form class for the given Messmethode based on its FieldDefinition objects.
    Returns a Bound form instance.
    """
    fields = {}
    for fd in messmethode.fields.all().order_by("order"):
        key = fd.name
        required = fd.required
        ft = fd.field_type
        meta = fd.meta or {}

        if ft == "text":
            fields[key] = forms.CharField(label=fd.label, required=required, widget=FIELD_WIDGETS["text"]())
        elif ft == "number":
            # use DecimalField to accept decimals
            fields[key] = forms.DecimalField(label=fd.label, required=required, widget=FIELD_WIDGETS["number"]())
        elif ft == "date":
            fields[key] = forms.DateField(
                label=fd.label,
                required=required,
                widget=FIELD_WIDGETS["date"](attrs={"type": "date"})
            )
        elif ft == "choice":
            # meta.choices can be stored as list of strings or list of tuples or comma-separated string
            choices = meta.get("choices", [])
            if isinstance(choices, str):
                # comma separated
                choices = [c.strip() for c in choices.split(",") if c.strip()]
            if choices and isinstance(choices[0], (list, tuple)):
                ctuple = choices
            else:
                ctuple = [(c, c) for c in choices]
            fields[key] = forms.ChoiceField(label=fd.label, required=required, choices=ctuple, widget=FIELD_WIDGETS["choice"]())
        elif ft == "file":
            fields[key] = forms.FileField(label=fd.label, required=required, widget=FIELD_WIDGETS["file"]())
        else:
            # fallback to CharField
            fields[key] = forms.CharField(label=fd.label, required=required, widget=FIELD_WIDGETS["text"]())

    DynamicForm = type("DynamicForm", (forms.Form,), fields)
    return DynamicForm(data=data, files=files)