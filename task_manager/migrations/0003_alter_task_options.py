# Generated by Django 5.1.1 on 2024-09-21 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0002_task_created_by"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={"ordering": ["-deadline"]},
        ),
    ]