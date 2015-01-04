from django.test import TestCase
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
