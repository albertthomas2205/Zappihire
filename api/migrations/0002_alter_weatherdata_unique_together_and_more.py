# Generated by Django 5.0.6 on 2024-06-13 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='weatherdata',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='location',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.RemoveField(
            model_name='weatherdata',
            name='country',
        ),
    ]
