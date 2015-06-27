from django.test import TestCase
from phonebook.models import Contact
from phonebook.forms import LoginForm, ContactForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class ContactTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user_test", password="password_test")

    def test_login(self):
        """Test login user"""
        response = self.client.login(username=self.user.username, password='password_test')
        self.assertTrue(response)

    def test_login_fail(self):
        """Test fail login user"""
        response = self.client.login(username=self.user.username, password='test_password')
        self.assertFalse(response)

    def test_login_form(self):
        form_data = {'username': self.user.username, 'password': 'test_password'}
        form = LoginForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_login_page_form(self):
        """Test login user"""
        response = self.client.post(reverse('phonebook_login_page'),
                                    {'username': self.user.username, 'password': 'password_test'})
        self.assertRedirects(response, reverse('phonebook_lists_contacts'))

    def test_login_page_form_fail(self):
        """Test fail login user"""
        response = self.client.post(reverse('phonebook_login_page'),
                                    {'username': self.user.username, 'password': 'test_password'})
        self.assertContains(response, 'Username or password is not correct.')

    def test_contact_create(self):
        """Create a contact"""
        contact = Contact.objects.create(firstname='Test firstname', lastname='Test lastname', email='test@test.fr',
                                         user_id=self.user)
        self.assertIsNotNone(contact)
        self.assertEquals(str(contact), "Test firstname Test lastname")
        self.assertEquals(unicode(contact), "Test firstname Test lastname")

    def test_contact_form(self):
        form_data = {
            'firstname': 'Test firstname',
            'lastname': 'Test lastname',
            'email': 'test@test.fr',
        }
        form = ContactForm(data=form_data)
        self.assertEqual(form.is_valid(), True)


class ContactViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user_test", password="password_test")
        self.client.login(username=self.user.username, password='password_test')
        self.contact = Contact.objects.create(firstname='Test firstname', lastname='Test lastname',
                                              email='test@test.fr', phone='0606060606', user_id=self.user)
        self.assertIsNotNone(self.contact)

    def test_call_login_redirect(self):
        response = self.client.get(reverse('phonebook_login_page'))
        self.assertRedirects(response, reverse('phonebook_lists_contacts'))

    def test_call_view_lists_contacts(self):
        response = self.client.get(reverse('phonebook_lists_contacts'))
        self.assertEqual(response.status_code, 200)

    def test_call_view_edit_contact(self):
        response = self.client.get(reverse('phonebook_edit', kwargs={'contact_id': self.contact.id}))
        self.assertEqual(response.status_code, 200)

    def test_call_view_post_edit_contact(self):
        response = self.client.post(reverse('phonebook_edit', kwargs={'contact_id': self.contact.id}),
                                    {'firstname': self.contact.firstname, 'lastname': self.contact.lastname,
                                     'email': self.contact.email})
        self.assertRedirects(response, reverse('phonebook_lists_contacts'))

    def test_call_view_post_new_contact(self):
        response = self.client.post(reverse('phonebook_new_contact'), {'firstname': 'Tesst new firstname',
                                                                       'lastname': 'Test new lastname',
                                                                       'email': 'test@newtest.fr'})
        self.assertRedirects(response, reverse('phonebook_lists_contacts'))

    def test_call_view_get_new_contact(self):
        response = self.client.get(reverse('phonebook_new_contact'))
        self.assertRedirects(response, reverse('phonebook_lists_contacts'))

    def test_call_view_call(self):
        response = self.client.get(reverse('phonebook_call', kwargs={'num': self.contact.phone}))
        self.assertEqual(response.status_code, 200)

    def test_call_view_exports_contacts(self):
        response = self.client.get(reverse('phonebook_exports_contacts'))
        self.assertEqual(response.status_code, 200)

    def test_call_view_delete_contact(self):
        response = self.client.get(reverse('phonebook_delete', kwargs={'contact_id': self.contact.id}))
        self.assertRedirects(response, reverse('phonebook_lists_contacts'))

    def test_call_logout(self):
        response = self.client.get(reverse('phonebook_logout'))
        self.assertRedirects(response, reverse('phonebook_login_page'))

    def test_call_view_edit_contact_with_fail(self):
        response = self.client.get(reverse('phonebook_edit', kwargs={'contact_id': 9999}))
        self.assertRedirects(response, reverse('phonebook_lists_contacts'))

    def test_call_view_post_search_contact(self):
        response = self.client.post(reverse('phonebook_search_contact'), {'query': 'test@newtest.fr'})
        self.assertRedirects(response, reverse('phonebook_search_contact_query', kwargs={'query': 'test@newtest.fr'}))

    def test_call_view_get_search_contact(self):
        response = self.client.get(reverse('phonebook_search_contact'))
        self.assertRedirects(response, reverse('phonebook_lists_contacts'))

