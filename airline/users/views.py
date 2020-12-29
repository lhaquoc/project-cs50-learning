from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

LOGIN_PAGE = "users/login.html"

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, LOGIN_PAGE, {
                "message": "Invalid credentials."
            })
    return render(request, LOGIN_PAGE)

def logout_view(request):
    logout(request)
    return render(request, LOGIN_PAGE, {
        "message": "Logged out."
    })