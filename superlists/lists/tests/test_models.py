from django.test import TestCase
from lists.models import Item, List


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
