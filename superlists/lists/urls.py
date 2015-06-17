from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('lists.views',
    url(r'^(\d+)/$', 'view_list', name="view_list"),
    url(r'^new$', 'new_list2', name='new_list'),
    url(r'^users/(.+)/$', 'my_lists', name='my_lists'),
)
