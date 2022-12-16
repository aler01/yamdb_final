from rest_framework import serializers

from .models import ROLES, User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Недопустимое имя')
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с данным username уже существует'
            )
        return data


class TokenSerializer(serializers.Serializer):

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    role = serializers.ChoiceField(choices=ROLES, default='user')

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
            'confirmation_code'
        )
        extra_kwargs = {
            'confirmation_code': {'write_only': True},
            'username': {'required': True},
            'email': {'required': True}
        }

        def validate_username(self, username):
            if username == 'me':
                raise serializers.ValidationError(
                    'Недопустимое имя'
                )
            return username
