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
        new_item_text = "A new list item"
        request.POST["item_text"] = new_item_text

        response = home_page(request)

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == new_item_text

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = "A new list item"

        response = home_page(request)

        assert response.status_code == 302
        assert response['Location'] == "/"

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        assert Item.objects.count() == 0

    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text="item1")
        Item.objects.create(text="item2")

        request = HttpRequest()
        response = home_page(request)

        content = response.content.decode()
        assert "item1" in content
        assert "item2" in content


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
