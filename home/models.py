from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime
import random
from django.urls import reverse


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    invitel = models.CharField(max_length=50)
    upline = models.CharField(max_length=100, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            super(User, self).save()
            self.invitel = ('refM=' + str(self.id))
        super(User, self).save()

    def __str__(self):
        return (self.invitel)


class Prospect(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('initiated', 'Initiated'),
        ('declined', 'Declined'),
        ('approved', 'Approved'),

    )
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending')
    code = models.CharField(max_length=100, null=True, blank=True)

    agent = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Document (models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='items')
    doc = models.FileField(upload_to='docs', null=True, blank=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    subject = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    message = models.TextField()
