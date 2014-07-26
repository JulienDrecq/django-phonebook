from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('phonebook',
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', 'views.view_login', name='phonebook_login_page'),
    url(r'^logout/', 'views.view_logout', name='phonebook_logout'),
    url(r'^lists_contacts/', 'views.view_lists_contacts', name='phonebook_lists_contacts'),
    url(r'^new_contact/', 'views.view_new_contact', name='phonebook_new_contact'),
    url(r'^delete/(?P<contact_id>\d+)/$', 'views.view_delete', name='phonebook_delete'),
    url(r'^edit/(?P<contact_id>\d+)/$', 'views.view_edit_contact', name='phonebook_edit'),
    url(r'^call/(?P<num>\d+)/$', 'views.view_call', name='phonebook_call'),
)