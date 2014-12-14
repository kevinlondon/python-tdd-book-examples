from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        assert found.func == home_page

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html")
        assert response.content.decode() == expected_html


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        lst = List.objects.create()
        Item.objects.create(text="item1", list=lst)
        Item.objects.create(text="item2", list=lst)

        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')


class NewListTest(TestCase):

    def test_saving_a_post_request(self):
        data = {"item_text": "A new list item"}
        response = self.client.post("/lists/new", data=data)

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == "A new list item"

    def test_redirects_after_POST(self):
        data = {"item_text": "A new list item"}
        response = self.client.post("/lists/new", data=data)

        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        lst = List()
        lst.save()

        first_text = "The first (ever) list item"
        second_text = "Item the second"
        first_item = Item.objects.create(text=first_text, list=lst)
        second_item = Item.objects.create(text=second_text, list=lst)

        saved_list = List.objects.first()
        assert saved_list == lst

        saved_items = Item.objects.all()
        assert saved_items.count() == 2
        assert saved_items[0].text == first_text
        assert saved_items[0].list == lst
        assert saved_items[1].text == second_text
        assert saved_items[1].list == lst
