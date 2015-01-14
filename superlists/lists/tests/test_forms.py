from django.test import TestCase
from lists.models import Item, List
from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm
)


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        data = form.as_p()
        assert 'placeholder="Enter a to-do item"' in data
        assert 'class="form-control input-lg"' in data

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={"text": ""})
        assert form.is_valid() is False
        assert form.errors['text'] == [EMPTY_ITEM_ERROR]

    def test_form_save_handles_saving_to_list(self):
        lst = List.objects.create()
        form = ItemForm(data={"text": "do this"})
        new_item = form.save(for_list=lst)
        assert new_item == Item.objects.first()
        assert new_item.text == "do this"
        assert new_item.list == lst


class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        lst = List.objects.create()
        form = ExistingListItemForm(for_list=lst)
        assert 'placeholder="Enter a to-do item"' in form.as_p()

    def test_form_validation_for_blank_items(self):
        lst = List.objects.create()
        form = ExistingListItemForm(for_list=lst, data={"text": ""})
        assert form.is_valid() is False
        assert form.errors['text'] == [EMPTY_ITEM_ERROR]

    def test_form_save_handles_saving_to_list(self):
        lst = List.objects.create()
        Item.objects.create(list=lst, text="no twins!")
        form = ExistingListItemForm(for_list=lst, data={"text": "no twins!"})
        assert form.is_valid() is False
        assert form.errors['text'] == [DUPLICATE_ITEM_ERROR,]

    def test_form_save(self):
        lst = List.objects.create()
        form = ExistingListItemForm(for_list=lst, data={"text": "hi"})
        new_item = form.save()
        assert new_item == Item.objects.all().first()
