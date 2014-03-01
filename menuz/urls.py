from django.conf.urls import patterns, include, url

from menuz import registry
registry.autodiscover()

urlpatterns = patterns('menuz.views',
    url(r'^menuz/reload/(?P<container_id>[\d+])/$', 'reload_menuz',
        name='reload_menuz'),
    url(r'^menuz/add_menuz/', 'add_menuz', name='add_menuz'),
    url(r'^menuz/reorder/', 'reorder_menuz', name='reorder_menuz'),
    url(r'^menuz/delete/', 'delete_menuz', name='delete_menuz'),
    url(r'^menuz/update/', 'update_menuz', name='update_menuz'),
)
