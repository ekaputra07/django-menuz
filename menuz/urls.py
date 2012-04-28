from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('menuz.views',
    url(r'^menuz/add_menuz/','add_menuz' , name='add_menuz'),
    url(r'^menuz/reorder/','reorder_menuz' , name='reorder_menuz'),
    url(r'^menuz/delete/','delete_menuz' , name='delete_menuz'),
    url(r'^menuz/update/','update_menuz' , name='update_menuz'),
)

