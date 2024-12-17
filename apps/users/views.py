from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.services import AuthenticationService
from django.core.exceptions import ValidationError
from users.models import CustomUser


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user:
            # Check if account is locked
            if user.is_account_locked():
                return Response(
                    {"error": "Account is locked. Try again later."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Validate login attempts
            try:
                AuthenticationService.validate_login_attempts(user)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Login successful"
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )
        
class MFAVerificationView(APIView):
    def post(self, request):
        email = request.data.get("email")
        mfa_token = request.data.get("mfa_token")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.mfa_secret and AuthenticationService.verify_mfa_token(user.mfa_secret, mfa_token):
            return Response({"message": "MFA verified successfully", "verified": True}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid MFA token", "verified": False}, status=status.HTTP_400_BAD_REQUEST)