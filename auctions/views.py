from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

from . import forms
from .models import Listing, User, WatchList
from auctions.templatetags import filters


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        form = forms.ListingForm(request.POST)
        new_listing = form.save(commit=False)
        new_listing.user = request.user
        new_listing.save()
        return HttpResponseRedirect(reverse("active_listing"))
    else:
        return render(
            request,
            "auctions/create_listing.html",
            {"form": forms.ListingForm()},
        )


def active_listing(request):
    listings = Listing.objects.all()
    return render(request, "auctions/active_listing.html", {"listings": listings})


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    current_price = filters.current_price(listing)
    if request.method == "POST":
        form = forms.BidForm(request.POST)
        new_bid = form.save(commit=False)
        if current_price > new_bid.bid_price:
            message = _("Bid price must be higher than current price")
            return render(
                request,
                "auctions/listing.html",
                {
                    "listing": listing,
                    "form": forms.BidForm(),
                    "message": message,
                },
            )
        else:
            current_price = new_bid.bid_price
            new_bid.user = request.user
            new_bid.item = listing
            new_bid.save()
    return render(
        request,
        "auctions/listing.html",
        {"listing": listing, "form": forms.BidForm()},
    )


def watch(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    try:
        new_watch = WatchList(user=user, listing=listing)
        new_watch.save()
    except IntegrityError:
        current_watch = WatchList.objects.filter(user=user).filter(listing=listing)
        current_watch.delete()
        label = "Add to watchlist"
        return render(
            request,
            "auctions/listing.html",
            {"listing": listing, "form": forms.BidForm(), "label": label},
        )
    else:
        label = "Remove from watchlist"
        return render(
            request,
            "auctions/listing.html",
            {"listing": listing, "form": forms.BidForm(), "label": label},
        )
