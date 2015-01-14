from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        assert item.text == ""

    def test_item_is_related_to_list(self):
        lst = List.objects.create()
        item = Item()
        item.list = lst
        item.save()
        self.assertIn(item, lst.item_set.all())

    def test_cannot_save_emepty_list_items(self):
        lst = List.objects.create()
        item = Item(list=lst, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        lst = List.objects.create()
        Item.objects.create(list=lst, text="bla")
        with self.assertRaises(ValidationError):
            item = Item(list=lst, text="bla")
            item.full_clean()

    def test_can_save_same_item_to_different_lists(self):
        lst = List.objects.create()
        lst2 = List.objects.create()
        Item.objects.create(list=lst, text="bla")
        item = Item(list=lst2, text="bla")
        item.full_clean()  # Should not raise error

    def test_list_ordering(self):
        lst = List.objects.create()
        item1 = Item.objects.create(list=lst, text="i1")
        item2 = Item.objects.create(list=lst, text="item 2")
        item3 = Item.objects.create(list=lst, text="3")
        assert list(Item.objects.all()) == [item1, item2, item3]

    def test_string_rep(self):
        item = Item(text="some text")
        assert str(item) == "some text"


class ListModelTest(TestCase):

    def test_absolute_url(self):
        lst = List.objects.create()
        self.assertEquals(lst.get_absolute_url(), "/lists/%d/" % lst.id)
