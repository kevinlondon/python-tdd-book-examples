from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import ItemForm, ExistingListItemForm
from .models import Item, List

def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request, list_id):
    lst = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=lst)

    if request.method == "POST":
        form = ExistingListItemForm(for_list=lst, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(lst)

    return render(request, "list.html", {"list": lst, "form": form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        lst = List.objects.create()
        form.save(for_list=lst)
        return redirect(lst)
    else:
        return render(request, "home.html", {"form": form})


def my_lists(request, email):
    return render(request, 'my_lists.html')
