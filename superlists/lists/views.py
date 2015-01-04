from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import ItemForm
from .models import Item, List

def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request, list_id):
    lst = List.objects.get(id=list_id)
    error = None

    if request.method == "POST":
        try:
            item = Item(text=request.POST['text'], list=lst)
            item.full_clean()
            item.save()
            return redirect(lst)
        except ValidationError:
            error = "You can't have an empty list item"
            return render(request, "home.html", {"error": error})

    return render(request, "list.html", {"list": lst, "error": error})


def new_list(request):
    lst = List.objects.create()
    item = Item(text=request.POST['text'], list=lst)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        lst.delete()
        error = "You can't have an empty list item"
        return render(request, "home.html", {"error": error})

    return redirect(lst)
