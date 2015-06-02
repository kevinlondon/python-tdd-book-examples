import unittest
from unittest import skip
from django.core.urlresolvers import resolve
from django.utils.html import escape
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
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

class NewListTest(TestCase):

    def test_saving_a_post_request(self):
        data = {"text": "A new list item"}
        response = self.client.post("/lists/new", data=data)

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == "A new list item"

    def test_redirects_after_POST(self):
        data = {"text": "A new list item"}
        response = self.client.post("/lists/new", data=data)
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % new_list.pk)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        assert response.status_code == 200
        self.assertTemplateUsed(response, "home.html")

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        self.client.post("/lists/new", data={"text": ""})
        assert List.objects.count() == 0
        assert Item.objects.count() == 0

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        data = {"text": "A new item for an existing list"}
        self.client.post('/lists/%d/' % correct_list.pk, data=data)
        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == "A new item for an existing list"
        assert new_item.list == correct_list

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        data = {"text": "A new item for an existing list"}
        response = self.client.post('/lists/%d/' % correct_list.pk, data=data)
        self.assertRedirects(response, '/lists/%d/' % correct_list.pk)


class MyListsTest(TestCase):

    def test_my_lists_url_renders_my_lists_template(self):
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')
