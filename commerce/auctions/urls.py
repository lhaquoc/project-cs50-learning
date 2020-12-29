from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_auction", views.add_auction, name="add_auction"),
    path("category/<str:person>/<str:category>", views.category_view, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("my_listings/<str:user>", views.my_listings, name="my_listings"),
    path("auction/<str:auction>", views.auction_view, name="auction_view")
]
