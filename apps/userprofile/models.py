from django.db import models
from django.contrib.auth.models import User
from djstripe.models import Subscription
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


class Userprofile(models.Model):
    BASIC = 'basic'
    PRO = 'pro'

    CHOICES_PLAN = (
        (BASIC, 'Basic'),
        (PRO, 'Pro')
    )

    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=20, null=True)
    logo = models.ImageField(null=True, blank=True)
    company = models.CharField(max_length=20, null=True)

    # plan = models.CharField(max_length=20, choices=CHOICES_PLAN, default='BASIC')

    # subscription = models.CharField(max_length=100, default='0')

    # logo = models.ImageField(default='./img/spie.png', upload_to='images/')

# def isPro(self):
# subscription = Subscription.objects.get(id=self.subscription)

# return subscription.status
