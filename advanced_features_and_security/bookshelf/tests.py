from django.test import TestCase
from .models import CustomUser  # Adjust the import based on your custom user model's location

class CustomUserModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
            date_of_birth='2000-01-01',
            profile_photo=None  # Adjust if you have a default or mock image
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.date_of_birth, '2000-01-01')
        self.assertIsNone(self.user.profile_photo)

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')  # Adjust based on your __str__ method

    def test_user_permissions(self):
        # Assuming you have set up permissions, test if the user has the correct permissions
        self.user.user_permissions.add('can_view')  # Adjust based on your permission setup
        self.assertTrue(self.user.has_perm('app_name.can_view'))  # Replace 'app_name' with your app's name

# Additional tests can be added here for other models and functionalities as needed.