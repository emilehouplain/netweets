# Generated by Django 3.2.9 on 2022-01-03 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_auto_20220103_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jeu',
            name='win',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cT3', to='game.comptetwitter'),
        ),
    ]
