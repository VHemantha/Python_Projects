from cgitb import html
from logging.handlers import TimedRotatingFileHandler
from django.shortcuts import render
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
from markdown2 import Markdown
import difflib

#i have get help of youtube code example for below edit function codes

class newEntry(forms.Form):
    title = forms.CharField(label='Title', widget=forms.Textarea(attrs={"style": "height:50px; width:99%;", 'class': 'form-control'}))
    content = forms.CharField(label='Markdown Content', widget=forms.Textarea(attrs={"style": "height:550px; width:99%;", 'class': 'form-control'}))

markdowner=Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def title(request, name):

    data = util.get_entry(name)
    if data == None:
        return render(request, "encyclopedia/404.html")
    return render(request, "encyclopedia/title.html", {
        "title":name, "data":markdowner.convert(data)
    })

def search(request):
    print(request.GET)
    query_dict = request.GET
    query = query_dict.get("q")
    data = util.get_entry(query)
    if data == None:
        entries = util.list_entries()
        f_data = difflib.get_close_matches(query, entries, cutoff=0.1)
        title = "search result"
        return render(request, "encyclopedia/search.html", {
        "data":f_data, "title":title})
    else:
        f_data = data
        title =  query
        return render(request, "encyclopedia/search.html", {
        "data":markdowner.convert(f_data), "title":title})


def newpage(request):
    if request.method == 'POST':
        form = newEntry(request.POST)
        print(form.is_valid())
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            data = util.get_entry(title)
            if data != None:
                return render(request, "encyclopedia/error.html")  
            else:       
                util.save_entry(title,  f'# {title}\n\n{content}')
                return HttpResponseRedirect(reverse('title', kwargs={'name':title}))
        else:
            form = newEntry()
            return render(request, "encyclopedia/newentry.html", {
            "form": form
            })
    else:
        form = newEntry()
    return render(request, "encyclopedia/newentry.html", {
        "form": form
    })

def editpage(request):
    if request.method == "POST":
        title = request.POST["edit"]
        data = util.get_entry(title)
        
    return render(request, "encyclopedia/editpage.html", {
        "title" : title,
        "content":data
    })

def saveedit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
    return render(request, "encyclopedia/title.html", {
        "title":title, "data":content
    })

def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    content = markdowner.convert(util.get_entry(random_title))
    return render(request, "encyclopedia/title.html", {
        "title":random_title, "data":content
    })