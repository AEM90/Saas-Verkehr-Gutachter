"""Lightweight registry for field types and helpers.

Add field types here; this module is intentionally small and migration-free.
"""

FIELD_TYPES = [
    ("text", "Text"),
    ("date", "Date"),
    ("number", "Number"),
    ("boolean", "Boolean"),
    ("choice", "Choice"),
    ("email", "Email"),
    ("textarea", "Textarea"),
]

def choices():
    """Return a list of (value, label) pairs for model/form choice use."""
    return list(FIELD_TYPES)

def is_boolean(ftype):
    return ftype == "boolean"

def render_value(value, ftype):
    if ftype == "boolean":
        return "Yes" if value else "No"
    return "" if value is None else str(value)
