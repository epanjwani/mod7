# Generated by Django 3.0.5 on 2020-04-18 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='user',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
