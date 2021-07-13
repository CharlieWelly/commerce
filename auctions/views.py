from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required

from . import forms
from .models import Listing, User, WatchList, CloseBid, Comment
from auctions.templatetags import filters


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings})


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(
            request,
            "auctions/create_listing.html",
            {"form": forms.ListingForm()},
        )


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "bid_form": forms.BidForm(),
            "comment_form": forms.CommentForm(),
            "comments": listing.item_comments.all(),
        },
    )


@login_required(login_url="login")
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    last_bid = listing.bids.last()
    form = forms.BidForm(request.POST)
    bid = form.save(commit=False)
    if last_bid and bid.bid_price <= last_bid.bid_price:
        message = "bid price must be higher than current price"
    elif not last_bid and bid.bid_price < listing.start_bid:
        message = "bid price must be at least start price"
    else:
        bid.user = request.user
        bid.item = listing
        bid.save()
        message = "Biding successfully"
    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "bid_form": forms.BidForm(),
            "comment_form": forms.CommentForm(),
            "comments": listing.item_comments.all(),
            "message": message,
        },
    )


@login_required(login_url="login")
def watch(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    try:
        new_watch = WatchList(user=user, listing=listing)
        new_watch.save()
    except IntegrityError:
        current_watch = WatchList.objects.filter(user=user).filter(listing=listing)
        current_watch.delete()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def close_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if listing.bids.last():
        CloseBid.objects.create(listing=listing, bid=listing.bids.last())
    else:
        CloseBid.objects.create(listing=listing)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url="login")
def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    form = forms.CommentForm(request.POST)
    comment = form.save(commit=False)
    comment.user = request.user
    comment.item = listing
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url="login")
def watch_list(request):
    user = request.user
    watch_list = user.watching.all()
    return render(
        request,
        "auctions/index.html",
        {"listings": [entry.listing for entry in watch_list]},
    )


def categories(request):
    return render(
        request, "auctions/categories.html", {"categories": list(Listing.Categories)}
    )


def category(request, category_value):
    return render(
        request,
        "auctions/index.html",
        {"listings": Listing.objects.filter(categories=category_value)},
    )
