from api.serializers import UserSerializer
from companies.serializers import CompanyReadModelSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import UsersRequests

User = get_user_model()

class UsersRequestsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersRequests
        fields = '__all__'
        read_only_fields = ('user', )
        
    # Automatically assign user_id with authenticated user
    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['user'] = user
        return super().create(validated_data)


class UsersRequestsReadSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = CompanyReadModelSerializer()

    class Meta:
        model = UsersRequests
        fields = '__all__'
        read_only_fields = ('user', )
