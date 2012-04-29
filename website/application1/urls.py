from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
                       (r'^$', 'application1.views.home'),
                       (r'^createUser', 'application1.views.createUser'),
                       (r'^login', 'application1.views.login_view'),
                       (r'^logout', 'application1.views.logout_view'),
                       (r'^submitEntry', 'application1.views.create_entry'),
                       (r'^test', 'application1.views.test'),
                       (r'get', 'application1.views.get_entry'),
                       (r'scrape', 'application1.views.scrape'),
#    'psets.views',
#    (r'^$', 'index'),
#    (r'^create/$', 'create_pset'),
#    (r'^pset/(?P<pset_id>\d+)/$', 'pset_detail'),
#    (r'^pset/(?P<pset_id>\d+)/add_question/$', 'add_question'),
)




