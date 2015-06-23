from django.test import TestCase
from phonebook.models import Contact
from django.contrib.auth.models import User


class ContactTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="user_test", password="password_test")

    def test_login(self):
        """Test login user"""
        user = User.objects.get(username="user_test")
        response = self.client.login(username=user.username, password='password_test')
        self.assertTrue(response)

    def test_login_fail(self):
        """Test fail login user"""
        user = User.objects.get(username="user_test")
        response = self.client.login(username=user.username, password='test_password')
        self.assertFalse(response)

    def test_contact_create(self):
        """Create a contact"""
        user = User.objects.get(username="user_test")
        contact = Contact.objects.create(firstname='Test firstname', lastname='Test lastname', email='test@test.fr',
                                         user_id=user)
        self.assertIsNotNone(contact)
