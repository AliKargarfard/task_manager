from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from apps.core.permissions import IsOwnerOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()