from django.contrib import admin
from .models import User, Category, Person, Auction, Bid, Comment, PersonalWatchlist
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(PersonalWatchlist)
admin.site.register(Person)