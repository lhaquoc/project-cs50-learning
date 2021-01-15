from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    name = "Quoc"
    context = {
        "name": name,
    }
    return render(request, "polls/index.html", context)