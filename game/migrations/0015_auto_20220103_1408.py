# Generated by Django 3.2.9 on 2022-01-03 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_alter_jeu_win'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jeu',
            name='compteTwitter1',
        ),
        migrations.RemoveField(
            model_name='jeu',
            name='compteTwitter2',
        ),
        migrations.RemoveField(
            model_name='jeu',
            name='win',
        ),
    ]