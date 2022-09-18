import random

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect


from markdown2 import Markdown
from . import util




def entry(request, title):
    html_content = conv_mark_to_html(title)

    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry dose not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "content" : html_content
        })


def conv_mark_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)





def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })




def serach(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = conv_mark_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            recommendation = []
            allEntries = util.list_entries()
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })




def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exist"
            })
        else:
            util.save_entry(title, content)
            html_content = conv_mark_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })




def edit_page(request):
    title = request.POST["entry_title"]
    content = util.get_entry(title)
    if request.method == "POST":
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content

        })



def save_edit(request):
    title = request.POST["title"]
    content = request.POST["content"]
    util.save_entry(title, content)
    html_content = conv_mark_to_html(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })




def random_page(request):
    enties = util.list_entries()
    random_entry = random.choice(enties)
    return redirect("entry", random_entry)

