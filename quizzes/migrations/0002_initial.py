# Generated by Django 4.2.5 on 2023-09-24 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0001_initial'),
        ('quizzes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='quizmark',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_mark', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quiz',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='rooms.examroom'),
        ),
        migrations.AlterUniqueTogether(
            name='quizmark',
            unique_together={('quiz', 'student')},
        ),
        migrations.AlterUniqueTogether(
            name='quiz',
            unique_together={('room', 'title')},
        ),
    ]
