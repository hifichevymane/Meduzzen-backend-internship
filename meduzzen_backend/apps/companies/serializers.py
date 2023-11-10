from api.serializers import UserSerializer
from django.contrib.auth import get_user_model
from quizzes.models import QuizResult
from rest_framework import serializers

from companies.enums import CompanyInvitationStatus
from companies.models import Company, CompanyInvitations, CompanyMembers, CompanyUserRating

User = get_user_model()

class CompanyWriteModelSerializer(serializers.ModelSerializer):
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


class CompanyReadModelSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True}
        }


class CompanyInvitationsModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    company = serializers.SerializerMethodField(method_name='get_company')

    class Meta:
        model = CompanyInvitations
        fields = '__all__'
        read_only_fields = ('company', 'user')
    
    def get_user(self, obj):
        # If method is POST we recieve user id
        if self.context['request'].method == 'POST':
            return obj.user_id
        else: # Display all user info
            user = User.objects.get(pk=obj.user_id)
            return UserSerializer(user).data
    
    def get_company(self, obj):
        # If method is POST we recieve user id
        if self.context['request'].method == 'POST':
            return obj.company_id
        else: # Display all user info
            company = Company.objects.get(pk=obj.company_id)
            return CompanyReadModelSerializer(company).data

    def create(self, validated_data):
        company_id = self.context['request'].data.get('company')
        user_id = self.context['request'].data.get('user')
        
        company = Company.objects.get(pk=company_id)
        user = User.objects.get(pk=user_id)

        validated_data['company'] = company
        validated_data['user'] = user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if validated_data['status'] == CompanyInvitationStatus.ACCEPTED.value:
            # Automatically add new company member
            CompanyMembers.objects.create(company=instance.company, user=instance.user)

        return super().update(instance, validated_data)


class CompanyMembersWriteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMembers
        fields = '__all__'


class CompanyMembersReadModelSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = CompanyReadModelSerializer()

    class Meta:
        model = CompanyMembers
        fields = '__all__'


class CompanyUserRatingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUserRating
        fields = '__all__'
        read_only_fields = ('avarage_score', )

    # Calculate avarage score of the user within the company
    def update(self, instance, validated_data):
        user = self.context['request'].user
        users_quiz_results = QuizResult.objects.filter(user=user, company=instance.company)

        avarage_score = 0
        sum_all_correct_answers = 0 # all correct answers
        sum_total_questions = 0 # all answered questions

        for result in users_quiz_results:
            sum_all_correct_answers += result.score
            sum_total_questions += result.quiz.question_amount
        
        # Calculate the avarage score
        avarage_score = sum_all_correct_answers / sum_total_questions
        instance.avarage_score = avarage_score

        return super().update(instance, validated_data)
