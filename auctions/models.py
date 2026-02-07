from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank = True, related_name = "user_watchlist")
    pass

class Category(models.Model):
    category = models.CharField(max_length = 16)

    def __str__(self):
        return self.category

class Listing(models.Model):
    title = models.CharField(max_length = 16)
    description = models.CharField(max_length = 128)
    image = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
    is_active = models.BooleanField(default = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "listing_category")
    seller = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "listing_user")

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bid_user")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "bid_listing")
    price = models.PositiveIntegerField(default = 0)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comment_user")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "comment_listing")
    comment = models.CharField(max_length = 128)