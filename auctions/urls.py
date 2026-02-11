from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("view_listing/<int:listing>", views.view_listing, name="view_listing"),
    path("change_watchlist/<int:listing>", views.change_watchlist, name="change_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:listing>", views.bid, name="bid"),
    path("comment/<int:listing>", views.comment, name="comment"),
    path("close_listing/<int:listing>", views.close_listing, name="close_listing"),
    path("won_auctions", views.won_auctions, name="won_auctions"),
    path("categories", views.categories, name="categories"),
    path("view_category/<int:category>", views.view_category, name="view_category")
]
