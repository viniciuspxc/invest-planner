# Generated by Django 4.2.11 on 2024-04-03 23:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_investment_starting_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='starting_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
