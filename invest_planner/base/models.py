from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']


class Investment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=200, default='Investimento Title')
    starting_amount = models.FloatField()
    number_of_years = models.FloatField()
    return_rate = models.FloatField()
    annual_additional_contribution = models.FloatField()

    def __str__(self):
        return self.title
