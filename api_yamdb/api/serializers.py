from rest_framework import serializers

from users.models import User

class SingUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено!')
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
