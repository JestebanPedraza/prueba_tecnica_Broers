from rest_framework.viewsets import ModelViewSet
from users.models import User
from crud.api.serializer import UserSerializer
from rest_framework.permissions import IsAdminUser


class UserApiViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
