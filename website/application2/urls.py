from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    (r'^$', 'application2.views.home'),
    (r'^post_id', 'application2.views.get_id'),

#    'psets.views',
#    (r'^$', 'index'),
#    (r'^create/$', 'create_pset'),
#    (r'^pset/(?P<pset_id>\d+)/$', 'pset_detail'),
#    (r'^pset/(?P<pset_id>\d+)/add_question/$', 'add_question'),
)




