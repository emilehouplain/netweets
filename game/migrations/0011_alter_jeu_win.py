# Generated by Django 3.2.9 on 2021-12-29 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_rename_game_jeu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jeu',
            name='win',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aaa', to='game.comptetwitter'),
        ),
    ]
