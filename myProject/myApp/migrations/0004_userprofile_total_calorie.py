# Generated by Django 5.0.2 on 2024-02-14 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0003_remove_userprofile_total_calorie'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='total_calorie',
            field=models.FloatField(null=True),
        ),
    ]