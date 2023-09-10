# Generated by Django 4.1.3 on 2023-09-10 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("occuring_date", models.DateField()),
                ("from_time", models.TimeField()),
                ("to_time", models.TimeField()),
                ("total_marks", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="rooms.examroom"
                    ),
                ),
            ],
            options={"unique_together": {("room", "title")},},
        ),
    ]
