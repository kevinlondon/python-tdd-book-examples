from django.core.urlresolvers import resolve
from django.utils.html import escape
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

    def test_validation_errors_end_up_on_lists_page(self):
        lst = List.objects.create()
        response = self.client.post("/lists/%d/" % lst.pk,
                                    data={"item_text": ""})
        assert response.status_code == 200
        self.assertTemplateUsed(response, "list.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


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
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % new_list.pk)

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new", data={"item_text": ""})
        assert response.status_code == 200
        self.assertTemplateUsed(response, "home.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post("/lists/new", data={"item_text": ""})
        assert List.objects.count() == 0
        assert Item.objects.count() == 0

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        data = {"item_text": "A new item for an existing list"}
        self.client.post('/lists/%d/' % correct_list.pk, data=data)
        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == "A new item for an existing list"
        assert new_item.list == correct_list

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        data = {"item_text": "A new item for an existing list"}
        response = self.client.post('/lists/%d/' % correct_list.pk, data=data)
        self.assertRedirects(response, '/lists/%d/' % correct_list.pk)
