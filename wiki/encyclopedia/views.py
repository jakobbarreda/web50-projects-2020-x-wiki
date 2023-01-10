from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms

from random import randint

from . import util
from . import markdown2

import markdown2
markdown2.markdown("*boo!*")  # or use `html = markdown_path(PATH)`
'<p><em>boo!</em></p>\n'

from markdown2 import Markdown
markdowner = Markdown()
markdowner.convert("*boo!*")
'<p><em>boo!</em></p>\n'
markdowner.convert("**boom!**")
'<p><strong>boom!</strong></p>\n'


class NewForm(forms.Form):
    title = forms.CharField(label="title")

class AddEntry(forms.Form):
    # creating a title field
    title = forms.CharField(label="title")
    # creating a text area
    description = forms.CharField(widget=forms.Textarea)


def index(request):

    # show all the links to entrys
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    # converting markdown to html
    description = markdowner.convert(util.get_entry(title))

    # if the description exist then render the entry page for title
    if description:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "description": description
        })
    else:
        return render(request, "encyclopedia/error404.html")


def add(request):

    # if data was submitted
    if request.method == "POST":
        
        # creating a AddEntry form with user req data
        form = AddEntry(request.POST)

        # form is valid
        if form.is_valid():
            # creating title/desc variable from user input 
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            
            # if title is already in encyclopedia
            if title in util.list_entries():
                return HttpResponse("Entry Already Exist")

            # save the new title/description to entries
            util.save_entry(title, description)

            # return to entry page with title as argument
            return HttpResponseRedirect(reverse("entry", kwargs={"title":title}))
            
    # render page if user request page
    return render(request, "encyclopedia/add.html", {
        "add_form":AddEntry()
    })


# the edit page
def edit(request, title):

    if request.method == "POST":

        form = AddEntry(request.POST)

        # if valid create a new object with request data from user
        if form.is_valid():
            obj = AddEntry()
            obj.title = form.cleaned_data["title"]
            obj.description = form.cleaned_data["description"]
            util.save_entry(obj.title,obj.description)
            
            return HttpResponseRedirect(reverse("entry", kwargs={"title":title}))
    
    
    title = title
    description = util.get_entry(title)
    edit_form = AddEntry({"title":title,"description":description})
    

    return render(request, "encyclopedia/edit.html", {
        "edit_form":edit_form,
        "title":title,
        "description":description
    })


    

# the random page
def random(request):
    if request.method == "POST":
        pass

    # a function generating a random number
    def randomNumber():
        return randint(1,1000)

    # saving randomNumber()
    # getting len of entry lists
    random_number = randomNumber()
    entry_count = len(util.list_entries()) -1

    # dividing the number until it matches up with the list of entries
    while random_number > entry_count:
        # break loop if number is 1
        if random_number == 1:
            break
        random_number /= 2
    
    # getting title at number index location
    random_entry_title = util.list_entries()[int(random_number)]
    # getting description 
    entry_description = markdowner.convert(util.get_entry(random_entry_title))


    return render(request, "encyclopedia/random.html", {
        "random_entry":random_entry_title,
        "entry_description":entry_description
    })

def search(request):
    
    if request.method == "POST":

        entry_list = util.list_entries()
        # getting query from input name from form
        q = request.POST["q"]
        # if title not in entry list return search page
        if q not in entry_list:
            return render(request, "encyclopedia/search.html", {"q":q, "entry_list":entry_list})
        
        # else display the title/description
        return HttpResponseRedirect(reverse("entry", kwargs={"title":q}))
    # GET request
    return render(request, "encyclopedia/search.html")