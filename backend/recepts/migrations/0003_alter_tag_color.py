# Generated by Django 3.2.3 on 2023-07-29 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recepts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7),
        ),
    ]
