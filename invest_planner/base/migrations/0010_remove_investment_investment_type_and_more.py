# Generated by Django 4.2.11 on 2024-08-01 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_investment_investment_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='investment_type',
        ),
        migrations.AlterField(
            model_name='investment',
            name='rate_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
