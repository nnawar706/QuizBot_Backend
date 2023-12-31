from rest_framework import serializers
from django.conf import settings
from django.db import transaction
from .models import *
from quizzes.models import Quiz
from django.utils import timezone


class AnswerSerializer (serializers.Serializer):
    answer = serializers.CharField()
    status = serializers.IntegerField()


class SubQuestionSerializer (serializers.Serializer):
    question    = serializers.CharField()
    sub_mark    = serializers.FloatField()
    image_url   = serializers.CharField(required=False)
    answers     = AnswerSerializer(many=True, required=False)


class QuestionSerializer (serializers.Serializer):
    question_type_id = serializers.IntegerField()
    detail           = serializers.CharField(required=False)
    total            = serializers.FloatField()
    sub_questions    = SubQuestionSerializer(many=True)


class QuestionCreateSerializer(serializers.Serializer):
    quiz_id     = serializers.IntegerField()
    questions   = QuestionSerializer(many=True)

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        self.request = context.get('request')
        super().__init__(*args, **kwargs)

    def validate(self, data):
        try:
            quiz = Quiz.objects.get(pk=data['quiz_id'])
        except Quiz.DoesNotExist:
            raise serializers.ValidationError('Invalid quiz.')

        if quiz.occurring_date < timezone.now().date():
            raise serializers.ValidationError('The selected quiz has passed.')

        if quiz.questions.count() > 0:
            raise serializers.ValidationError('Question has already been created for this quiz.')

        if quiz.room.user != self.request.user:
            raise serializers.ValidationError('Cannot add questions to this quiz.')

        for question in data['questions']:
            sub_mark_total = sum(sub_question['sub_mark'] for sub_question in question['sub_questions'])

            if sub_mark_total != question['total']:
                raise serializers.ValidationError('Total of sub question marks must be equal to total marks of a question.')

            for sub_question in question['sub_questions']:
                answers = sub_question['answers']

                if len(answers) < 2:
                    raise serializers.ValidationError('Each sub questions must have at least 2 choices for answers.')

                if not any(answer['status'] == 1 for answer in answers):
                    raise serializers.ValidationError('Each sub question must have at least 1 correct answer.')

        return data

    def create (self, data):
        with transaction.atomic():
            for question in data['questions']:
                ques = Question(
                    detail              = question['detail'],
                    total               = question['total'],
                    question_type_id    = question['question_type_id'],
                    quiz_id             = data['quiz_id']
                )

                ques.save()

                for sub_question in question['sub_questions']:
                    sub_ques = SubQuestion(
                        ques        = sub_question['question'],
                        sub_mark    = sub_question['sub_mark'],
                        image_url   = sub_question.get('image_url', None),
                        question    = ques
                    )

                    sub_ques.save()

                    for answer in sub_question['answers']:
                        ans = SubQuestionAnswer(
                            answer          = answer['answer'],
                            status          = answer['status'],
                            sub_question    = sub_ques
                        )

                        ans.save()



class AnswerSubQuestionsSerializer(serializers.Serializer):
    answers = serializers.ListField()

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        self.request = context.get('request')
        self.sq = context.get('sq')
        super().__init__(*args, **kwargs)

    def validate (self, data):
        existing_answer = self.sq.marks.filter(student=self.request.user).first()

        if existing_answer:
            raise serializers.ValidationError('You have already submitted answer for this question.')

        return data

    def store_answer (self, data):
        answers = self.sq.answers.all()
        given_answers = data['answers']
        correct_answers = [answer.id for answer in answers if answer.status]

        correct_answers.sort()
        given_answers.sort()

        with transaction.atomic():

            sq_mark = SubQuestionMark(
                mark = self.sq.sub_mark if correct_answers == given_answers else 0,
                sub_question   = self.sq,
                student        = self.request.user
            )

            sq_mark.save()

            for given_answer in given_answers:
                sq_student_answer = SubQuestionStudentAnswer(
                    sub_question_student_mark = sq_mark,
                    answer_id                 = given_answer
                )

                sq_student_answer.save()

        return data


# class RetrieveQuizMarkSerializer (serializers.Serializer):
#     class Meta:



# model serializers

class AnswerModelSerializerWithStatus (serializers.ModelSerializer):

    class Meta:
        model = SubQuestionAnswer
        fields = '__all__'


class AnswerModelSerializer (serializers.ModelSerializer):

    class Meta:
        model = SubQuestionAnswer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        send_status = context.get('send_answers')
        if send_status is False:
            del self.fields['status']
        super().__init__(*args, **kwargs)



class SubQuestionModelSerializer (serializers.ModelSerializer):

    class Meta:
        model = SubQuestion
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['answers'] = AnswerModelSerializer(instance.answers.all(), many=True, context=self.context).data
        return data

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        self.send_status = context.get('send_answers')
        super().__init__(*args, **kwargs)


class QuestionTypeModelSerializer (serializers.ModelSerializer):

    class Meta:
        model = QuestionType
        fields = '__all__'


class RetrieveQuestionModelSerializer (serializers.ModelSerializer):
    question_type   = QuestionTypeModelSerializer(many=False, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sub_questions'] = SubQuestionModelSerializer(instance.sub_questions.all(), many=True, context=self.context).data
        return data


    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        self.send_status = context.get('send_answers')
        super().__init__(*args, **kwargs)
