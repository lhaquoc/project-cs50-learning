from django.urls import path
from . import views

urlpatterns = [
    # "" means /index, "something" means /index/something
    path("", views.index, name="index"), 
    # <str:variable> means /index/variable, get variable 
    path("<str:name>", views.greet, name="greet")
]