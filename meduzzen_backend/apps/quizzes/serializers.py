from rest_framework import serializers

from quizzes.models import AnswerOption, Question, Quiz, QuizResult, UserQuizStatus, UsersAnswer


class QuizModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ('creator', 'question_amount')
    
    def validate_questions(self, value):
        # Check if there are at least 2 questions and more
        if len(value) < 2:
            raise serializers.ValidationError('there must be at least two questions in the quiz')
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        questions = self.context['request'].data.get('questions')
        
        validated_data['creator'] = user
        # Automatically assign amount of questions
        validated_data['question_amount'] = len(questions)
        return super().create(validated_data)


class QuestionModelSerializer(serializers.ModelSerializer):
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
            raise serializers.ValidationError('there must be at least two answer options in the question')
        return value


class AnswerOptionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = '__all__'
        read_only_fields = ('creator', )

    # Automaticaly assign current user as the creator
    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['creator'] = user
        return super().create(validated_data)


class QuizResultModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = '__all__'
        read_only_fields = ('user', 'score', 'company', 'quiz')
    
    # Automatically assign user with current user
    def create(self, validated_data):
        user = self.context['request'].user
        quiz_id = self.context['request'].data.get('quiz')
        quiz = Quiz.objects.get(pk=quiz_id)
        company = quiz.company
        
        validated_data['company'] = company
        validated_data['user'] = user
        validated_data['quiz'] = quiz
        return super().create(validated_data)

    # Calculate score when quiz is completed
    def update(self, instance, validated_data):
        user = self.context['request'].user

        all_users_correct_answers = UsersAnswer.objects.filter(
            quiz_id=instance.quiz.id, 
            user=user, quiz_result=instance.pk,
            is_correct=True
        )
        
        instance.score = len(all_users_correct_answers)
        instance.status = UserQuizStatus.COMPLETED.value

        return super().update(instance, validated_data)


class UsersAnswerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersAnswer
        fields = '__all__'
        read_only_fields = ('user', 'is_correct')

    def create(self, validated_data):
        user = self.context['request'].user
        question = validated_data['question']
        user_question_answer = validated_data['answer']

        correct_answer_list = list(question.answer.all())

        # Check if this answer is correct
        validated_data['is_correct'] = True if user_question_answer == correct_answer_list else False
        # Automatically assign user with current user
        validated_data['user'] = user
        return super().create(validated_data)
