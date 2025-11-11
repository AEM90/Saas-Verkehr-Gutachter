from django.test import TestCase
from django import forms
from .models import Messmethode, FieldDefinition
from .forms import build_form_for_messmethode
from companies.models import Company


class BooleanFieldTypeTestCase(TestCase):
    """Test that boolean field type is correctly mapped to BooleanField"""
    
    def setUp(self):
        # Create a test company and messmethode
        self.company = Company.objects.create(
            name="Test Company",
            slug="test-company"
        )
        self.messmethode = Messmethode.objects.create(
            company=self.company,
            name="Test Method",
            slug="test-method"
        )
    
    def test_boolean_field_creation(self):
        """Test that a boolean field definition creates a BooleanField"""
        # Create a boolean field definition
        field_def = FieldDefinition.objects.create(
            messmethode=self.messmethode,
            name="accepts_terms",
            label="Accept Terms and Conditions",
            field_type="boolean",
            required=True,
            order=1
        )
        
        # Build the form
        form = build_form_for_messmethode(self.messmethode)
        
        # Check that the field exists and is a BooleanField
        self.assertIn("accepts_terms", form.fields)
        self.assertIsInstance(form.fields["accepts_terms"], forms.BooleanField)
        self.assertEqual(form.fields["accepts_terms"].label, "Accept Terms and Conditions")
        self.assertTrue(form.fields["accepts_terms"].required)
        
    def test_boolean_field_with_checkbox_widget(self):
        """Test that boolean field uses CheckboxInput widget"""
        field_def = FieldDefinition.objects.create(
            messmethode=self.messmethode,
            name="newsletter_opt_in",
            label="Subscribe to newsletter",
            field_type="boolean",
            required=False,
            order=1
        )
        
        # Build the form
        form = build_form_for_messmethode(self.messmethode)
        
        # Check the widget type
        self.assertIsInstance(
            form.fields["newsletter_opt_in"].widget,
            forms.CheckboxInput
        )

