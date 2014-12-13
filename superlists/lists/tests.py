from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        assert found.func == home_page

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html")
        assert response.content.decode() == expected_html

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST["item_text"] = "A new list item"
        response = home_page(request)
        assert "A new list item" in response.content.decode()

        expected_html = render_to_string(
            "home.html",
            {"new_item_text": "A new list item"}
        )
        assert response.content.decode() == expected_html


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_text = "The first (ever) list item"
        second_text = "Item the second"
        first_item = Item.objects.create(text=first_text)
        second_item = Item.objects.create(text=second_text)
        saved_items = Item.objects.all()
        assert saved_items.count() == 2
        assert saved_items[0].text == first_text
        assert saved_items[1].text == second_text
