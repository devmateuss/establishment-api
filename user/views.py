from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .models import UserProfile
from rest_framework import viewsets, status
from .serializers import UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def sign_up(self, request):
        data = request.data

        if data['email']:
            if not UserProfile.objects.filter(email=data['email']).exists():
                user = UserProfile.objects.create_user(
                    username=data['email'],
                    email=data['email'],
                    password=data['password']
                )

                Token.objects.get_or_create(user=user)

                return JsonResponse({
                    'success': True,
                    'message': 'Cadastro efetuado com sucesso',
                    'token': user.auth_token.key
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'E-mail já cadastrado.!',
                    'status': 201
                })
        else:
            return Response('Login inválido.', status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def sign_in(self, request):
        data = request.data

        user = authenticate(
            password=data['password'],
            username=(UserProfile.objects.values_list('username', flat=True)
                      .filter(email=data['email']).first())
        )

        if user:
            return JsonResponse({
                'success': True,
                'message': 'Login efetuado com sucesso',
                'token': user.auth_token.key
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Senha incorreta ou usuário incorreto ou não encontrado.',
            })
