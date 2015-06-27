from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from phonebook.forms import LoginForm, ContactForm, SearchForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from phonebook.models import Contact
from django.db.models import Q
from phonebook import settings
from django.http import HttpResponse
import csv
from datetime import datetime
import re

URL_RENDER = {
    'view_login': 'phonebook/login.html',
    'view_lists_contacts': 'phonebook/lists_contacts.html',
    'view_edit_contact': 'phonebook/edit_contact.html',
    'view_call': 'phonebook/call.html',
}


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        query = or_query
    return query


def view_login(request):
    error = False
    login_form = LoginForm()

    if request.user.is_authenticated():
        return redirect(reverse(view_lists_contacts), locals())

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse(view_lists_contacts))
            else:
                error = True
    return render(request, URL_RENDER['view_login'], locals())


def view_logout(request):
    logout(request)
    return redirect(reverse(view_login))


LOGIN_URL = view_login


@login_required(login_url=LOGIN_URL)
def view_lists_contacts(request):
    newcontact_form = ContactForm()
    search_form = SearchForm()
    URL_CLICK_TO_CALL = str(settings.URL_CLICK_TO_CALL).replace(' ', '')
    contacts = Contact.objects.filter(Q(user_id=request.user)).order_by('id')
    return render(request, URL_RENDER['view_lists_contacts'], locals())


@login_required(login_url=LOGIN_URL)
def view_search_contact(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            query = search_form.cleaned_data["query"]
            return redirect(reverse(view_search_contact_query, kwargs={'query': query}))
    return redirect(reverse(view_lists_contacts))


@login_required(login_url=LOGIN_URL)
def view_search_contact_query(request, query):
    newcontact_form = ContactForm()
    search_form = SearchForm()
    URL_CLICK_TO_CALL = str(settings.URL_CLICK_TO_CALL).replace(' ', '')
    contacts = Contact.objects.filter(
        get_query(query, ['firstname', 'lastname', 'email', 'phone', 'mobile_phone'])).order_by('id')
    return render(request, URL_RENDER['view_lists_contacts'], locals())



@login_required(login_url=LOGIN_URL)
def view_new_contact(request):
    if request.method == 'POST':
        newcontact_form = ContactForm(request.POST)
        if newcontact_form.is_valid():
            firstname, lastname = newcontact_form.cleaned_data["firstname"], newcontact_form.cleaned_data["lastname"]
            email, phone = newcontact_form.cleaned_data["email"], newcontact_form.cleaned_data["phone"]
            mobile_phone = newcontact_form.cleaned_data["mobile_phone"]
            contact = Contact(firstname=firstname, lastname=lastname, email=email, phone=phone,
                              mobile_phone=mobile_phone, user_id=request.user)
            contact.save()
            return redirect(reverse(view_lists_contacts))
    return redirect(reverse(view_lists_contacts))


@login_required(login_url=LOGIN_URL)
def view_delete(request, contact_id):
    contact = Contact.objects.filter(Q(user_id=request.user, id=contact_id))
    if contact:
        contact.delete()
    return redirect(reverse(view_lists_contacts))


@login_required(login_url=LOGIN_URL)
def view_edit_contact(request, contact_id):
    contact = Contact.objects.filter(Q(user_id=request.user, id=contact_id))
    if not contact:
        return redirect(reverse(view_lists_contacts), locals())
    contact = contact[0]
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            firstname, lastname = contact_form.cleaned_data["firstname"], contact_form.cleaned_data["lastname"]
            email, phone = contact_form.cleaned_data["email"], contact_form.cleaned_data["phone"]
            mobile_phone = contact_form.cleaned_data["mobile_phone"]
            contact.firstname, contact.lastname, contact.email = firstname, lastname, email
            contact.phone, contact.mobile_phone = phone, mobile_phone
            contact.save()
            return redirect(reverse(view_lists_contacts))
    else:
        contact_form = ContactForm(initial={
            'firstname': contact.firstname,
            'lastname': contact.lastname,
            'email': contact.email,
            'phone': contact.phone,
            'mobile_phone': contact.mobile_phone,
        })
    return render(request, URL_RENDER['view_edit_contact'], locals())


@login_required(login_url=LOGIN_URL)
def view_call(request, num=0):
    url_click_to_call = str(settings.URL_CLICK_TO_CALL) + str(num)
    return render(request, URL_RENDER['view_call'], locals())


@login_required(login_url=LOGIN_URL)
def exports_contacts(request):
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="exports_contacts_%s.csv"' % \
                                      datetime.now().strftime('%Y%m%d_%H%M%S')
    writer = csv.writer(response)
    writer.writerow(['Firstname', 'Lastname', 'Email', 'Phone', 'Mobile phone'])
    contacts = Contact.objects.filter(Q(user_id=request.user)).order_by('id')
    for contact in contacts:
        writer.writerow([contact.firstname, contact.lastname, contact.email, contact.phone, contact.mobile_phone])
    return response


