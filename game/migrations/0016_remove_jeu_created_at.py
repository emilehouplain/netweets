# Generated by Django 3.2.9 on 2022-01-03 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0015_auto_20220103_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jeu',
            name='created_at',
        ),
    ]