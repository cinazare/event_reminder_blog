# Generated by Django 5.0.6 on 2024-07-01 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='financial_credit',
            field=models.IntegerField(default=0),
        ),
    ]