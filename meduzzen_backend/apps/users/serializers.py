from api.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import UsersRequests

User = get_user_model()

class UsersRequestsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField() # Display all user information

    class Meta:
        model = UsersRequests
        fields = '__all__'
        read_only_fields = ('user', )

    def get_user(self, obj):
        # If method is POST we recieve user id
        if self.context['request'].method == 'POST':
            return obj.user_id
        else: # Display all user info
            user = User.objects.get(pk=obj.user_id)
            return UserSerializer(user).data
        
    # Automatically assign user_id with authenticated user
    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['user'] = user
        return super().create(validated_data)
