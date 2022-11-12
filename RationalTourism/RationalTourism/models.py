from django.db import models


class User(models.Model):
    username = models.CharField(default='', max_length=20)
    token = models.CharField(primary_key=True, max_length=15)
    score = models.IntegerField(default=0)


class Target(models.Model):
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)


class InteractiveScreen(models.Model):
    question = models.CharField(max_length=200, default='')
    level = models.IntegerField(default=0)
    locked = models.BooleanField(default='False')
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    target = models.ForeignKey(Target, on_delete=models.CASCADE, blank=True, null=True)

