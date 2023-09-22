# Generated by Django 4.1.3 on 2023-09-22 05:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="examroomhasstudents",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="examroom",
            name="students",
            field=models.ManyToManyField(
                related_name="student",
                through="rooms.ExamRoomHasStudents",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="examroom",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rooms",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="examroomhasstudents", unique_together={("room", "student")},
        ),
        migrations.AlterUniqueTogether(
            name="examroom", unique_together={("user", "title")},
        ),
    ]