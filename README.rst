**Django Phonebook**

**Design with Bootstrap v3 framework**
(http://getbootstrap.com/)

Phonebook is a simple Django app to manage contacts (lastname, firstname, mail, phone, mobile phone) and integred ``click2call`` .
Application development and testing with django v1.7.6


.. contents:: Contents
    :depth: 3

Quick start
-----------

1. Add ``phonebook`` to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'phonebook',
      )

2. Include the phonebook URLconf in your project urls.py like this::

      url(r'^phonebook/', include('phonebook.urls')),

3. Run ``python manage.py syncdb`` to create the phonebook models.

4. Start the development server and visit ``http://127.0.0.1:8000/phonebook/`` to start phonebook.


Optional parameters
-------------------

1. Change url for click2call in ``phonebook/settings.py`` ::

    URL_CLICK_TO_CALL = getattr(settings, 'URL_CLICK_TO_CALL', 'http://my_url_click_to_call?num=')
    
    If you do not use the click2call, do not change the ``phonebook/settings.py`` .
    
    
2. This application is translated. add ``LANGUAGE_CODE`` , ``LANGUAGES`` , ``LOCALE_PATHS`` , ``MIDDLEWARE_CLASSES``  , ``TEMPLATE_CONTEXT_PROCESSORS`` in ``settings.py`` ::

        LANGUAGE_CODE = 'en'
        USE_I18N = True
        USE_L10N = True
        
        from django.utils.translation import gettext_lazy as _
        LANGUAGES = (
            ...
            ('en', _('English')),
            ('fr', _('French')),
        )
        
        LOCALE_PATHS = (
            os.path.join(BASE_DIR, 'phonebook/locale')
        )
        
        
        MIDDLEWARE_CLASSES = (
            ...
            'django.middleware.locale.LocaleMiddleware',
        )
        
        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            'django.core.context_processors.i18n',
        )

TODO
----

    - Search field contact
    - Create, edit, delete groups on contacts
    - Exports contacts
