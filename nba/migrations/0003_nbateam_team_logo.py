# Generated by Django 5.0.6 on 2024-05-30 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0002_alter_nbagame_home_pts_alter_nbagame_visitor_pts'),
    ]

    operations = [
        migrations.AddField(
            model_name='nbateam',
            name='team_logo',
            field=models.ImageField(default=1, upload_to='logos/nba'),
            preserve_default=False,
        ),
    ]
