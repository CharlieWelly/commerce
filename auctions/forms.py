from django.forms import (
    ModelForm,
    TextInput,
    Textarea,
    NumberInput,
    URLInput,
    FileInput,
    Select,
)
from .models import Listing, Bid, WatchList, Comment


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ["user"]
        widgets = {
            "title": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control", "rows": 4}),
            "start_bid": NumberInput(attrs={"class": "form-control"}),
            "url": URLInput(attrs={"class": "form-control"}),
            "categories": Select(attrs={"class": "form-control"}),
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_price"]
        widgets = {
            "bid_price": NumberInput(
                attrs={"class": "form-control", "placeholder": "Bid here"}
            )
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "type your comment here",
                    "rows": 1,
                }
            )
        }
