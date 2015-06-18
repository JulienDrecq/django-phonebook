from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from phonebook.models import Contact

admin.site.register(Contact)