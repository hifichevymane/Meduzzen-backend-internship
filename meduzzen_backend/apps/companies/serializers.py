from rest_framework.serializers import ModelSerializer

from companies.models import Company, CompanyInvitations, CompanyMembers


class CompanyModelSerializer(ModelSerializer):
    class Meta:
        model = Company
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


class CompanyInvitationsModelSerializer(ModelSerializer):
    class Meta:
        model = CompanyInvitations
        fields = '__all__'


class CompanyMembersModelSerializer(ModelSerializer):
    class Meta:
        model = CompanyMembers
        fields = '__all__'
    