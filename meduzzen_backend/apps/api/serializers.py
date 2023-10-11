from rest_framework import serializers

from api.models import User


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # All fields to work with
        fields = '__all__'
        extra_kwargs = {
            # Make these fields required
            'email': {'required': True},
            # Not display the password after creation
            'password': {'write_only': True, 'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    # Hashing the passsword
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user


# User Serializer for auth/users/me path
class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
