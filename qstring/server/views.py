from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from qstring.server.serializers import UserSerializer, GroupSerializer, LoginSerializer
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from django.views.decorators.csrf import csrf_exempt


class LoginView(APIView):
    @staticmethod
    def post(request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )

    @staticmethod
    def post(request):
        django_logout(request)
        return Response(status=204)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
