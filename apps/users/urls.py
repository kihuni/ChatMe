from django.urls import path
from users.views import UserRegistrationView, LoginView, MFAVerificationView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("verify-mfa/", MFAVerificationView.as_view(), name="mfa-verification"),

]
