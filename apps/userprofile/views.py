from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from djstripe.models import Product
from djstripe import settings
import stripe
import djstripe
from django.db import models
from django.contrib.auth.models import User
from djstripe.models import Subscription

from .models import Userprofile
from .form import UserProfileForm


@login_required
def changeToBasic(request, sub_id):
    subscription = Subscription.objects.get(id=self.subscription)
    subscription.plan = 'Basic'


@login_required
def changeToPro(self):
    subscription = Subscription.objects.get(id=self.subscription)
    subscription.plan = 'pro'
