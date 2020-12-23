from django.shortcuts import render
from django import forms
from markdown2 import Markdown
import random

from . import util

CREATE_PAGE = "encyclopedia/create.html"
INDEX_PAGE = "encyclopedia/index.html"
ENTRY_PAGE  = "encyclopedia/entry.html"
SEARCH_PAGE = "encyclopedia/search.html"
ERROR_PAGE = "encyclopedia/error.html"
EDIT_PAGE = "encyclopedia/edit.html"
ERROR_MESSAGE_NOT_FOUND = "The requested page was not found."
ERROR_MESSAGE_EXISTED = "Page already exist."

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'myfieldclass',
        'placeholder': 'Search'
    }))

class Post(forms.Form):
    title = forms.CharField(label='title')
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')

markdowner = Markdown()

def index(request):
    entries = util.list_entries()
    items = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdowner.convert(page)
                    
                    context = {
                        'page': page_converted,
                        'title': item,
                        'form': Search()
                    }
                    return render(request, ENTRY_PAGE, context)
                elif item.lower() in i.lower(): 
                    items.append(i)
                    context = {
                        'items': items, 
                        'form': Search()
                    }
                    return render(request, SEARCH_PAGE, context)
                else:
                    context = {
                        'items': items, 
                        'form': Search()
                    }
            return render(request, SEARCH_PAGE, context)
        else:
            return render(request, INDEX_PAGE, {"form": form})
    else:
        return render(request, INDEX_PAGE, {
            "entries": entries, "form":Search()
        })

""" def search(request):
    entries = util.list_entries()
    items = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdowner.convert(page)
                    context = {
                        'page': page_converted,
                        'title': item,
                        'form': Search()
                    }
                    return render(request, ENTRY_PAGE, context)
                if item.lower() in i.lower():
                    searched.append(i)
                    context = {
                        'items': items,
                        'form': Search()
                    }
                    return render(request, SEARCH_PAGE, context)
                context = {
                        'items': items,
                        'form': Search()
                    }
            return render(request, SEARCH_PAGE, context)
        else: 
            return render(request, INDEX_PAGE, { "form": form }) """

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdowner.convert(page)

        context = {
            'page': page_converted,
            'title': title,
            'form': Search()
        }
        return render(request, ENTRY_PAGE, context)
    else:
        error_context = {
            'message': ERROR_MESSAGE_NOT_FOUND,
            'form': Search()
        }
        return render(request, ERROR_PAGE, error_context)

def create(request):
    if request.method == 'POST':
        form = Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, ERROR_PAGE, {"form": Search(), "message": ERROR_MESSAGE_EXISTED})
            else:
                util.save_entry(title, textarea)
                page = util.get_entry(title)
                page_converted = markdowner.convert(page)
                context = {
                    'form': Search(),
                    'page': page_converted,
                    'title': title
                }
                return render(request, ENTRY_PAGE, context)
    else:
        context = {
            'form': Search(),
            'post': Post()
        }
        return render(request, CREATE_PAGE, context)

def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        context = {
            'form': Search(),
            'edit': Edit(initial={'textarea': page}),
            'title': title
        }
        return render(request, EDIT_PAGE, context)
    else:
        form = Edit(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title, textarea)
            page = util.get_entry(title)
            page_converted = markdowner.convert(page)

            context = {
                'form': Search(),
                'page': page_converted,
                'title': title
            }
        return render(request, ENTRY_PAGE, context)

def randomPage(request):
    if request.method == 'GET':
        entries = util.list_entries()
        num = random.randint(0, len(entries) - 1)
        page_random = entries[num]
        page = util.get_entry(page_random)
        page_converted = markdowner.convert(page)
        context = {
            'form': Search(),
            'page': page_converted,
            'title': page_random
        }
        return render(request, ENTRY_PAGE, context)