from django.shortcuts import render
from markdown2 import Markdown
import random
from . import myforms
from . import util

CREATE_PAGE = "encyclopedia/create.html"
INDEX_PAGE = "encyclopedia/index.html"
ENTRY_PAGE  = "encyclopedia/entry.html"
SEARCH_PAGE = "encyclopedia/search.html"
ERROR_PAGE = "encyclopedia/error.html"
EDIT_PAGE = "encyclopedia/edit.html"
FAQ_PAGE = "encyclopedia/faq.html"
ERROR_MESSAGE_NOT_FOUND = "The requested page was not found."
ERROR_MESSAGE_EXISTED = "Page already exist."

markdowner = Markdown()
search = myforms.Search()
post = myforms.Post()

def index(request):
    entries = util.list_entries()
    items = []
    if request.method == "POST":
        form = myforms.Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdowner.convert(page)
                    
                    context = {
                        'page': page_converted,
                        'title': item,
                        'form': search
                    }
                    return render(request, ENTRY_PAGE, context)
                elif item.lower() in i.lower(): 
                    items.append(i)
                    context = {
                        'items': items, 
                        'form': search
                    }
                    return render(request, SEARCH_PAGE, context)
                else:
                    context = {
                        'items': items, 
                        'form': search
                    }
            return render(request, SEARCH_PAGE, context)
        else:
            return render(request, INDEX_PAGE, {"form": form})
    else:
        return render(request, INDEX_PAGE, {
            "entries": entries, "form":search
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
                        'form': search
                    }
                    return render(request, ENTRY_PAGE, context)
                if item.lower() in i.lower():
                    searched.append(i)
                    context = {
                        'items': items,
                        'form': search
                    }
                    return render(request, SEARCH_PAGE, context)
                context = {
                        'items': items,
                        'form': search
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
            'form': search
        }
        return render(request, ENTRY_PAGE, context)
    else:
        error_context = {
            'message': ERROR_MESSAGE_NOT_FOUND,
            'form': search
        }
        return render(request, ERROR_PAGE, error_context)

def create(request):
    if request.method == 'POST':
        form = myforms.Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, ERROR_PAGE, {"form": search, "message": ERROR_MESSAGE_EXISTED})
            else:
                util.save_entry(title, textarea)
                page = util.get_entry(title)
                page_converted = markdowner.convert(page)
                context = {
                    'form': search,
                    'page': page_converted,
                    'title': title
                }
                return render(request, ENTRY_PAGE, context)
    else:
        context = {
            'form': search,
            'post': post
        }
        return render(request, CREATE_PAGE, context)

def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        context = {
            'form': search,
            'edit': myforms.Edit(initial={'textarea': page}),
            'title': title
        }
        return render(request, EDIT_PAGE, context)
    else:
        form = myforms.Edit(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title, textarea)
            page = util.get_entry(title)
            page_converted = markdowner.convert(page)

            context = {
                'form': search,
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
            'form': search,
            'page': page_converted,
            'title': page_random
        }
        return render(request, ENTRY_PAGE, context)

def faq(request):

    context = {
        'form': search,
    }
    return render(request, FAQ_PAGE, context)