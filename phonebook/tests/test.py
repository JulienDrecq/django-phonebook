from django.test import TestCase
from phonebook.models import Contact
from phonebook.forms import LoginForm, ContactForm
from django.contrib.auth.models import User


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

    def test_call_view_lists_contacts(self):
        self.client.login(username=self.user.username, password='password_test')
        response = self.client.get('/lists_contacts/')
        self.assertEqual(response.status_code, 200)
