# Generated by Django 3.2.9 on 2022-01-03 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_auto_20220103_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='jeu',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name='Date de création du jeu'),
        ),
    ]