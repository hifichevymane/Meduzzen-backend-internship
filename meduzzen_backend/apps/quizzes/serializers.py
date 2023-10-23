from rest_framework.serializers import ModelSerializer, ValidationError

from quizzes.models import AnswerOption, Question, Quiz


class QuizModelSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
    
    def validate_questions(self, value):
        # Check if there are at least 2 questions and more
        if len(value) < 2:
            raise ValidationError('there must be at least two questions in the quiz')
        return value


class QuestionModelSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('creator', )
    
    # Automaticaly assign current user as the creator
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['creator'] = user

        return super().create(validated_data)

    def validate_options(self, value):
        # Check if there are at least 2 answer options and more
        if len(value) < 2:
            raise ValidationError('there must be at least two answer options in the question')
        return value


class AnswerOptionModelSerializer(ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = '__all__'
        read_only_fields = ('creator', )

    # Automaticaly assign current user as the creator
    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['creator'] = user
        return super().create(validated_data)
