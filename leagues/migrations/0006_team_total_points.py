# Generated by Django 3.0.5 on 2020-04-20 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0005_remove_game_game_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='total_points',
            field=models.IntegerField(null=True),
        ),
    ]
