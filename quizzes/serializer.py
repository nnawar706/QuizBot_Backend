from rest_framework import serializers
from django.conf import settings
from django.utils import timezone
from rooms.models import ExamRoom
from .models import Quiz


class QuizCreateSerializer (serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = ['title', 'occurring_date', 'from_time', 'to_time', 'total_marks']

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        self.request = context.get('request')
        self.room = context.get('room')
        super().__init__(*args, **kwargs)

    def validate (self, data):
        room = self.room
        existing_quiz = Quiz.objects.filter(room=room, title=data['title']).first()

        if not room.status:
            raise serializers.ValidationError('Archived exam room cannot have a new quiz.')

        if existing_quiz:
            raise serializers.ValidationError('A quiz with the same title already exists.')

        if len(data['title']) < 3:
            raise serializers.ValidationError('Title field must be at least 5 characters long.')

        if data['occurring_date'] <= timezone.now().date():
            raise serializers.ValidationError('Quiz date must be greater than today.')

        if data['to_time'] < data['from_time']:
            raise serializers.ValidationError('End time should be greater than start time.')

        if data['total_marks'] < 10:
            raise serializers.ValidationError('Total marks must be at least 10.')

        return data

    def create (self, data):
        quiz = Quiz(
            room            = self.room,
            title           = data['title'],
            occurring_date  = data['occurring_date'],
            from_time       = data['from_time'],
            to_time         = data['to_time'],
            total_marks     = data['total_marks']
        )

        quiz.save()

        return quiz
