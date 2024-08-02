# Generated by Django 4.2.11 on 2024-08-02 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_remove_investment_investment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='rate_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='rate_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='rate_type',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]