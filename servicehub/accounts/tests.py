from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'role': 'customer' # Assuming custom user model needs this
        }

    def test_landing_page_unauthenticated(self):
        """Test that unauthenticated users see the landing page buttons."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Register')
        self.assertNotContains(response, 'Available Services')

    def test_registration_redirect(self):
        """Test that successful registration redirects to login."""
        # Using a valid form submission data
        # Note: We need to match the fields in CustomUserCreationForm.
        # Minimal viable test if we don't know exact form fields is checking the view logic
        # But let's try with standard fields + optional role if needed.
        # If this fails, I will inspect the form.
        response = self.client.post(self.register_url, self.user_data)
        
        # If validation fails, it renders form with errors (200). If success, redirect (302).
        if response.status_code == 200:
             print(response.context['form'].errors)

        self.assertRedirects(response, self.login_url)
        
        # Verify user is created
        self.assertTrue(User.objects.filter(username='testuser').exists())
        
        # Verify user is NOT logged in
        user = User.objects.get(username='testuser')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_redirect(self):
        """Test that login redirects to home."""
        # Create user first
        User.objects.create_user(**self.user_data)
        
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertRedirects(response, self.home_url)

    def test_home_page_authenticated(self):
        """Test that authenticated users see the dashboard/services."""
        self.client.login(username='testuser', password='testpassword123')
        User.objects.create_user(**self.user_data) # Re-create because setUp is per test but verification above might need it different
        # Actually setUp runs before EACH test.
        # So let's just log in.
        
        self.client.force_login(User.objects.create_user(**self.user_data))

        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Available Services')
        self.assertNotContains(response, 'Welcome to ServiceHub') 
