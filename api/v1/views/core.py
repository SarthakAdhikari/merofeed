from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from core.serializers import UserSerializer, AuthTokenSerializer

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_class = api_settings.DEFAULT_RENDERER_CLASSES
