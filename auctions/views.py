from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django import forms
from .models import *
from PIL import Image
from django.shortcuts import get_object_or_404

class CreateListingForm(ModelForm):
    price = forms.IntegerField() 

    class Meta:
        model = Listing
        fields = ["title", "description", "image", "category", "price"]

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active = True).all()
    }
)


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit = False)
            listing.seller = request.user
            listing.save()
            bid = Bid(
                price = request.POST["price"],
                user = request.user, 
                listing = listing)
            bid.save()
            if listing.image:
                img = Image.open(listing.image.path)
                output_size = (600, 600)
                img.resize(output_size)
                img.save(listing.image.path)
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html", {
        "form": CreateListingForm()
    }
)

def view_listing(request, listing):
    listing = get_object_or_404(Listing, id = listing)
    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = request.user.watchlist.filter(id = listing.id).exists()
    if request.method == "POST":
        if "change_watchlist" in request.POST and request.user.is_authenticated:
            if in_watchlist:
                request.user.watchlist.remove(listing)
            else:
                request.user.watchlist.add(listing)
            return HttpResponseRedirect(reverse("view_listing", args = (listing.id,)))
    return render(request, "auctions/view_listing.html", {
        "listing": listing,
        "in_watchlist": in_watchlist
    }
)

@login_required
def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    }
)