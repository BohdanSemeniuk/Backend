from rest_framework.generics import CreateAPIView

from .serializers import RegisterSerializer, LoginSerializer
from .permissions import IsUnauthenticated


class LoginAPIView(CreateAPIView):
    permission_classes = (IsUnauthenticated, )
    serializer_class = LoginSerializer


class RegisterAPIView(CreateAPIView):
    permission_classes = (IsUnauthenticated, )
    serializer_class = RegisterSerializer

