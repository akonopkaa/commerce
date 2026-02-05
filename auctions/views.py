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

class CreateListingForm(ModelForm):
    price = forms.IntegerField() 

    class Meta:
        model = Listing
        fields = ["title", "description", "image", "category", "price"]

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
    return render(request, "auctions/create_listing.html", {
        "form": CreateListingForm()
    }
)
