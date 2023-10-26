from quizzes.models import QuizResult
from rest_framework.serializers import ModelSerializer

from companies.models import Company, CompanyInvitations, CompanyMembers, CompanyUserRating


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


class CompanyUserRatingModelSerializer(ModelSerializer):
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
