# Generated by Django 3.2.9 on 2021-12-21 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20211221_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='lang',
            field=models.CharField(max_length=3000, null=True),
        ),
    ]
