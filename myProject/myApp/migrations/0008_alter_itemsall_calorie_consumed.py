# Generated by Django 5.0.2 on 2024-02-17 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0007_rename_total_calorie_userprofile_bmr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsall',
            name='calorie_consumed',
            field=models.FloatField(null=True),
        ),
    ]
