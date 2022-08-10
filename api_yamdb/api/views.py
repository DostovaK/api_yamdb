from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, permissions, status, viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import SingUpSerializer, UserSerializer
from api.permissions import IsAdmin
from users.models import User


class SignUp(APIView):
    def post(self, request):
        serializer = SingUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(User, username=serializer.data['username'])
            confirmation_code = default_token_generator.make_token(user)
            email = request.data.get('email')
            send_mail(
                'Код подтверждения',
                f'Ваш код: {confirmation_code}',
                from_email=None,
                recipient_list=email)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ('username')

    @action(
        methods=['get', 'patch',],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated,]
    )
    def my_profile(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
