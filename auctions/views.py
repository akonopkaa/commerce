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
from django.contrib import messages

class CreateListingForm(ModelForm):
    price = forms.IntegerField() 

    class Meta:
        model = Listing
        fields = ["title", "description", "image", "category", "price"]

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active = True).order_by("-id")
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
    
def view_listing(request, listing):
    listing = get_object_or_404(Listing, id = listing)
    comments = Comment.objects.filter(listing = listing)
    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = request.user.watchlist.filter(id = listing.id).exists()
    return render(request, "auctions/view_listing.html", {
        "listing": listing,
        "comments": comments,
        "in_watchlist": in_watchlist,
        "bid_form": BidForm(),
        "comment_form": CommentForm()
    }
)

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

@login_required
def change_watchlist(request, listing):
    if request.method == "POST":
        listing = get_object_or_404(Listing, id = listing)
        if listing in request.user.watchlist.all():
            request.user.watchlist.remove(listing)
        else:
            request.user.watchlist.add(listing)
        return HttpResponseRedirect(reverse("view_listing", args = (listing.id,)))
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    }
)

@login_required
def bid(request, listing):
    if request.method == "POST":
        listing = get_object_or_404(Listing, id = listing)
        try:
            price = int(request.POST["price"])
        except ValueError:
            messages.error(request, "Invalid price format.")
            return HttpResponseRedirect(reverse("view_listing", args = (listing,)))
        bid = Bid.objects.filter(listing = listing).order_by("-price").first()
        if price <= bid.price:
            messages.error(request, "Price must be higher than current bid.")
            return HttpResponseRedirect(reverse("view_listing", args = (listing.id,)))
        if request.user == listing.seller:
            messages.error(request, "Price must be higher than current bid.")
            return HttpResponseRedirect(reverse("view_listing", args = (listing.id,)))
        bid = Bid(
            user = request.user, 
            listing = listing,
            price = price)
        bid.save()
        messages.success(request, "Bid placed successfully!")
        return HttpResponseRedirect(reverse("view_listing", args = (listing.id,)))
    else:
        return HttpResponseRedirect(reverse("view_listing", args = (listing.id,)))

@login_required
def comment(request, listing):
    if request.method == "POST":
        listing = get_object_or_404(Listing, id = listing)
        comment = Comment(
            user = request.user, 
            listing = listing,
            comment = request.POST["comment"]
        )
        comment.save()
        messages.success(request, "Comment created successfully!")
        return HttpResponseRedirect(reverse("view_listing", args = (listing.id,)))
    else:
        return HttpResponseRedirect(reverse("view_listing", args = (listing.id,)))