# Generated by Django 5.0.6 on 2024-07-08 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_alter_transaction_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='mode',
            field=models.CharField(choices=[('+', 'charge'), ('-', 'cunsumption')], default='+', max_length=255),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='mount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
