from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100, blank=True)
    lastName = models.CharField(max_length=100, blank=True)
    secondEmail = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    secondPhone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=2000, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class EmailOtpModel(models.Model):
    email = models.CharField(max_length=100, blank=False, null=False)
    otp = models.IntegerField(blank=False, null=False)
    validTime = models.DateTimeField(blank=False, null=False)


class phoneOtpModel(models.Model):
    phone = models.CharField(max_length=20, blank=False, null=False)
    otp = models.IntegerField(blank=False, null=False)
    validTime = models.DateTimeField(blank=False, null=False)
