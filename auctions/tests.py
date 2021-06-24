from django.test import TestCase
from django.forms.boundfield import BoundField

from . import forms

# Create your tests here.


class FormTestCase(TestCase):
    def test_form_fields(self):
        form = forms.ListingForm()
        fields = form.fields.values()
        for field in fields:
            with self.subTest(field=field):
                self.assertIsInstance(field, BoundField)
