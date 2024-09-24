# Generated by Django 5.1.1 on 2024-09-22 17:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0003_alter_task_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worker",
            name="position",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="task_manager.position",
            ),
        ),
    ]