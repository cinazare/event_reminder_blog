# Generated by Django 5.0.6 on 2024-07-08 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_user_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='123456', max_length=255),
        ),
    ]
