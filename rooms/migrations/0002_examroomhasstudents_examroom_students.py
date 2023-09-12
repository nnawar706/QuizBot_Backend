# Generated by Django 4.2.5 on 2023-09-12 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamRoomHasStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.examroom')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('room', 'student')},
            },
        ),
        migrations.AddField(
            model_name='examroom',
            name='students',
            field=models.ManyToManyField(related_name='student', through='rooms.ExamRoomHasStudents', to=settings.AUTH_USER_MODEL),
        ),
    ]