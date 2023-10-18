from rest_framework import serializers

from users.models import UsersRequests


class UsersRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersRequests
        fields = '__all__'
        read_only_fields = ('user', )
        
    # Automatically assign user_id with authenticated user
    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['user'] = user
        return super().create(validated_data)
