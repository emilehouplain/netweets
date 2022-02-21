# Generated by Django 3.2.9 on 2021-12-21 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20211221_1233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comptetwitter',
            old_name='screen_name',
            new_name='username',
        ),
        migrations.RenameField(
            model_name='tweet',
            old_name='nb_comments',
            new_name='nb_quote',
        ),
        migrations.AddField(
            model_name='comptetwitter',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='comptetwitter',
            name='id_compteTwitter',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='comptetwitter',
            name='last_scrap',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='comptetwitter',
            name='nb_listed',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='comptetwitter',
            name='profile_image_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='tweet',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name='Date de création du tweet'),
        ),
        migrations.AddField(
            model_name='tweet',
            name='nb_reply',
            field=models.IntegerField(null=True),
        ),
    ]