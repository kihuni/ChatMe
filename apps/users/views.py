from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser, Role
from .serializers import UserRegistrationSerializer, RoleSerializer
from .permissions import RoleBasedPermission
from .services import AuthenticationService

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=False, 
        methods=['POST'], 
        permission_classes=[AllowAny]
    )
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'user_id': user.id,
            'email': user.email,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

    @action(
        detail=False, 
        methods=['POST'], 
        permission_classes=[IsAuthenticated]
    )
    def generate_mfa_secret(self, request):
        secret = AuthenticationService.generate_mfa_secret()
        return Response({'mfa_secret': secret})

class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer