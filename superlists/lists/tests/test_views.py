import unittest
from unittest.mock import Mock, patch
from django.core.urlresolvers import resolve
from django.utils.html import escape
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.views import home_page, new_list
from lists.models import Item, List
from lists.forms import (
    ItemForm, EMPTY_ITEM_ERROR,
    ExistingListItemForm, DUPLICATE_ITEM_ERROR
)


class HomePageTest(TestCase):
    maxDiff = None

    def test_home_page_renders_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_uses_item_form(self):
        response = self.client.get("/")
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        lst = List.objects.create()
        response = self.client.get("/lists/%d/" % (lst.pk))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        correct_list = List.objects.create()
        Item.objects.create(text="item1", list=correct_list)
        Item.objects.create(text="item2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="othertext", list=other_list)

        response = self.client.get("/lists/%d/" % correct_list.pk)

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, "othertext")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get("/lists/%d/" % correct_list.pk)
        assert response.context['list'] == correct_list

    def post_invalid_input(self):
        lst = List.objects.create()
        return self.client.post("/lists/%d/" % lst.pk, data={"text": ""})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        assert Item.objects.count() == 0

    def test_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'list.html')

    def test_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        lst = List.objects.create()
        response = self.client.get("/lists/%d/" % lst.pk)
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        lst = List.objects.create()
        item1 = Item.objects.create(list=lst, text="textey")
        response = self.client.post("/lists/%d/" % lst.pk,
                                    data={"text": "textey"})
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        assert Item.objects.count() == 1


class NewListViewIntegratedTest(TestCase):

    def test_saving_a_post_request(self):
        data = {"text": "A new list item"}
        response = self.client.post("/lists/new", data=data)

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == "A new list item"

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        request = HttpRequest()
        request.user = User.objects.create(email='a@b.com')
        request.POST['text'] = 'new list item'
        new_list(request)
        lst = List.objects.first()
        assert lst.owner == request.user


@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()

    def test_passes_POST_data_to_new_list_form(self, new_list_form_mock):
        new_list(self.request)
        new_list_form_mock.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, new_list_form_mock):
        mock_form = new_list_form_mock.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
        self, redirect_mock, new_list_form_mock
    ):
        mock_form = new_list_form_mock.return_value
        mock_form.is_valid.return_value = True

        response = new_list(self.request)

        assert response == redirect_mock.return_value
        redirect_mock.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_renders_home_template_with_form_if_form_invalid(
        self, render_mock, new_list_form_mock
    ):
        mock_form = new_list_form_mock.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        assert response == render_mock.return_value
        render_mock.assert_called_once_with(self.request, 'home.html', {'form': mock_form})

    def test_does_not_save_if_form_invalid(self, new_list_form_mock):
        mock_form = new_list_form_mock.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        assert not mock_form.save.called


class MyListsTest(TestCase):

    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        assert response.context['owner'] == correct_user
