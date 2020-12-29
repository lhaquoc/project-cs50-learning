from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Auction, Category, Bid, Person, Comment, PersonalWatchlist


def index(request):
    auctions = Auction.objects.all().order_by('id').reverse()
    persons = Person.objects.all()
    user = request.user
    if user is not None:
        context = {
            'auctions': auctions,
            'persons': persons
        }
        return render(request, "auctions/index.html", context)
    my_watchlist = PersonalWatchlist.objects.get(user=request.user)
    totalAuctions = my_watchlist.auctions.count()
    context = {
        'auctions': auctions,
        'totalAuctions': totalAuctions,
        'my_watchlist': my_watchlist,
        'persons': persons
    }
    return render(request, "auctions/index.html", context)

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
        if request.user.is_authenticated:
            return redirect('index')
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

def category_view(request, category, person):
    category_name = Category.objects.get(name=category)
    person_name = Person.objects.get(person=person)
    auctions = Auction.objects.filter(category=category_name, person=person_name).order_by('id').reverse()
    persons = Person.objects.all()
    user = request.user

    if user.id is None:
        return render(request, "auctions/index.html")

    my_watchlist = PersonalWatchlist.objects.get(user=request.user)
    totalAuctions = my_watchlist.auctions.count()
    context = {
        'auctions': auctions,
        'category_name': category_name,
        'persons': persons,
        'totalAuctions': totalAuctions
    }
    return render(request, "auctions/category.html", context)

def add_auction(request):
    pass

def watchlist(request):
    pass

def my_listings(request):
    pass

def auction_view(request, auction):
    pass