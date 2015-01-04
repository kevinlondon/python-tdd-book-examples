from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import ItemForm
from .models import Item, List

def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request, list_id):
    lst = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=lst)
            return redirect(lst)

    return render(request, "list.html", {"list": lst, "form": form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        lst = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=lst)
        return redirect(lst)
    else:
        return render(request, "home.html", {"form": form})
