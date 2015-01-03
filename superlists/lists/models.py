from django.db import models
from django.core.urlresolvers import reverse

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey('List', default=None)


class List(models.Model):

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])
