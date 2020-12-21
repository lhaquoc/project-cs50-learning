from django.http import HttpResponse
from django.shortcuts import render

tasks = ["foo", "bar", "baz"]
# Create your views here.
def index(request):
    render(request, "tasks/index.html", {
        "task": tasks
    })