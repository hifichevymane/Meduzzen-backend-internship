from rest_framework import serializers

from companies.models import Company


# Company create serializer
class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'description')
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True}
        }

    # Automatically assign owner_id with authenticated user
    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['owner'] = user
        return super().create(validated_data)


# Company detail serializer
class CompanyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
