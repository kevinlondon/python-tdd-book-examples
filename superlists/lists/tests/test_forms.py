import unittest
from unittest.mock import patch, Mock
from django.test import TestCase

from django.test import TestCase
from lists.models import Item, List
from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm, NewListForm
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


class NewListFormTest(unittest.TestCase):

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_data_if_not_authed(self, create_list_mock):
        user = Mock(is_authenticated=lambda: False)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        create_list_mock.assert_called_once_with(first_item_text='new item text')

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_with_owner_is_authed(self, create_list_mock):
        user = Mock(is_authenticated=lambda: True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        create_list_mock.assert_called_once_with(first_item_text='new item text', owner=user)

    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_object(self, create_list_mock):
        user = Mock(is_authenticated=lambda: True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        response = form.save(owner=user)
        assert response == create_list_mock.return_value
