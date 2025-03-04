from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from rest_framework.response import Response
from users.api.serializer import UserRegisterSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         user = authenticate(username=username, password=password)

#         if user is not None:
#             if user.is_active:
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "El usuario está inactivo."}, status=status.HTTP_403_FORBIDDEN)
#         else:
#             return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)


# class UserView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User, email=serializer.validated_data['email'])
        serializer.send_password_reset_email(user)

        return Response(
            {"detail": "Se ha enviado un enlace de restablecimiento de contraseña a tu correo"},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            user = User.objects.get(pk=uidb64)
        except User.DoesNotExist:
            return Response(
                {"detail": "Usuario inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar token
        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Token inválido o expirado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {"detail": "Contraseña restablecida exitosamente"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
