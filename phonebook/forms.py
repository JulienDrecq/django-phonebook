from django import forms
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"), max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username'),
                                                             'required': '', 'tabindex': 1, 'autofocus': '1'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                      'placeholder': _('Password'),
                                                                                      'required': '', 'tabindex': 2}))


class ContactForm(forms.Form):
    firstname = forms.CharField(label=_("Firstname"), max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'required': '', 'tabindex': 1,
                                                              'autofocus': '1'}))
    lastname = forms.CharField(label=_("Lastname"), max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'required': '', 'tabindex': 2}))
    email = forms.EmailField(label=_("Email"), max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'required': '', 'tabindex': 3}))
    phone = forms.CharField(label=_("Phone"), max_length=100, required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control', 'tabindex': 4}))
    mobile_phone = forms.CharField(label=_("Mobile phone"), max_length=100, required=False,
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'tabindex': 5}))