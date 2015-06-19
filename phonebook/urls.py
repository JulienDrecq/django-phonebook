from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.i18n import javascript_catalog
admin.autodiscover()

js_info_dict = {
    'packages': ('phonebook',),
}

urlpatterns = [
    url(r'^jsi18n/$', javascript_catalog, js_info_dict),
]

urlpatterns += patterns('phonebook',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', 'views.view_login', name='phonebook_login_page'),
    url(r'^logout/', 'views.view_logout', name='phonebook_logout'),
    url(r'^lists_contacts/', 'views.view_lists_contacts', name='phonebook_lists_contacts'),
    url(r'^new_contact/', 'views.view_new_contact', name='phonebook_new_contact'),
    url(r'^delete/(?P<contact_id>\d+)/$', 'views.view_delete', name='phonebook_delete'),
    url(r'^edit/(?P<contact_id>\d+)/$', 'views.view_edit_contact', name='phonebook_edit'),
    url(r'^call/(?P<num>\d+)/$', 'views.view_call', name='phonebook_call'),
    url(r'^exports_contacts/$', 'views.exports_contacts', name='phonebook_exports_contacts'),
)