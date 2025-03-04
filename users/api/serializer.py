from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import User
from django.urls import reverse


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        # Encriptar password
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


User = get_user_model()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Verificar si el correo existe en la base de datos
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No existe un usuario con este correo electrónico")
        return value

    def send_password_reset_email(self, user):
        # Generar token de restablecimiento
        token = default_token_generator.make_token(user)

        # Construir URL de restablecimiento
        reset_url = self.context['request'].build_absolute_uri(
            reverse('password-reset-confirm',
                    kwargs={'uidb64': user.pk, 'token': token})
        )

        # Enviar correo electrónico
        send_mail(
            'Restablecimiento de Contraseña',
            f'Haz clic en el siguiente enlace para restablecer tu contraseña:\n{reset_url}',
            'tu_correo@gmail.com',
            [user.email],
            fail_silently=False,
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        # Verificar que ambos campos estén presentes
        if 'new_password' not in data or 'confirm_password' not in data:
            raise serializers.ValidationError(
                "Debe proporcionar nueva contraseña y confirmación")

        # Verificar que las contraseñas coincidan
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")

        # Importante: SIEMPRE retornar los datos validados
        return data
