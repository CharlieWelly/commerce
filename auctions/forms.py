from django.forms import ModelForm, TextInput, Textarea, NumberInput, URLInput
from .models import Listing


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ["user"]
        widgets = {
            "title": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control"}),
            "start_bid": NumberInput(attrs={"class": "form-control"}),
            "url": URLInput(attrs={"class": "form-control"}),
        }
