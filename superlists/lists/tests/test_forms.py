from django.test import TestCase
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


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

