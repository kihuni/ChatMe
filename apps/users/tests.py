from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Role
from users.models import CustomUser
from users.services import AuthenticationService
import pyotp

class UserRegistrationAPITests(APITestCase):
    def setUp(self):
        self.role = Role.objects.create(name=3, description="Regular Member")
        self.valid_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "password123",
            "confirm_password": "password123",
            "role": self.role.id,
        }
        self.url = "/api/register/"

    def test_valid_registration(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "testuser@example.com")

    def test_invalid_password_mismatch(self):
        self.valid_data["confirm_password"] = "mismatched_password"
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirm_password", response.data)
        
class MFATokenVerificationTests(APITestCase):
    def setUp(self):
        self.role = Role.objects.create(name=3, description="Regular Member")
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            full_name="Test User",
            password="password123",
            role=self.role,
        )
        self.secret = AuthenticationService.generate_mfa_secret()
        self.url = "/api/verify-mfa/"

    def test_valid_mfa_token(self):
        totp = pyotp.TOTP(self.secret)
        token = totp.now()
        response = self.client.post(self.url, {"email": self.user.email, "mfa_token": token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["verified"])

    def test_invalid_mfa_token(self):
        response = self.client.post(self.url, {"email": self.user.email, "mfa_token": "wrong_token"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["verified"])

class UserRegistrationAPITests(APITestCase):
    def setUp(self):
        self.role = Role.objects.create(name=3, description="Regular Member")
        self.valid_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "password123",
            "confirm_password": "password123",
            "role": self.role.id,
        }
        self.url = "/api/register/"

    def test_valid_registration(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "testuser@example.com")

    def test_invalid_password_mismatch(self):
        self.valid_data["confirm_password"] = "mismatched_password"
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirm_password", response.data)

class MFATokenVerificationTests(APITestCase):
    def setUp(self):
        self.role = Role.objects.create(name=3, description="Regular Member")
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            full_name="Test User",
            password="password123",
            role=self.role,
        )
        self.secret = AuthenticationService.generate_mfa_secret()
        self.url = "/api/verify-mfa/"

    def test_valid_mfa_token(self):
        totp = pyotp.TOTP(self.secret)
        token = totp.now()
        response = self.client.post(self.url, {"email": self.user.email, "mfa_token": token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["verified"])

    def test_invalid_mfa_token(self):
        response = self.client.post(self.url, {"email": self.user.email, "mfa_token": "wrong_token"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["verified"])
