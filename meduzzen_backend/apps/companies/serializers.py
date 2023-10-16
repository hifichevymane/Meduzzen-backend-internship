from rest_framework.serializers import ModelSerializer

from companies import models


# Company serializer
class CompanyModelSerializer(ModelSerializer):
    class Meta:
        model = models.Company
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True}
        }

    # Automatically assign owner_id with authenticated user
    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['owner'] = user
        return super().create(validated_data)


# CompaniesRequests Model serializer
class CompanyRequestsModelSerializer(ModelSerializer):
    class Meta:
        model = models.CompanyRequests
        fields = '__all__'


class CompanyMembersModelSerializer(ModelSerializer):
    class Meta:
        model = models.CompanyMembers
        fields = '__all__'
    