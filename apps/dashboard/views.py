from django.http import HttpResponse
import djstripe.settings
from djstripe.settings import djstripe_settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
import djstripe
from .models import PricingCategory
from .forms import PricingForm
import stripe
from django.http import JsonResponse
from djstripe.models import Product
from djstripe import settings
from django.views.decorators.csrf import csrf_exempt
from apps.userprofile.models import Userprofile
from apps.userprofile.form import UserProfileForm


# Create your views here.
@login_required
def more_info_user(request):
    user = request.user.userprofile
    # print(user)
    form = UserProfileForm(instance=user)
    # print(form)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'The form has been Updated')

            return redirect('testzone')
    else:
        form = UserProfileForm(instance=user)

    context = {
        'form': form
    }
    return render(request, 'dashboard/more_info_user.html', context)


@login_required
def dashboard(request):
    PricingCategories = request.user.PricingCategories.all()
    print(PricingCategories)

    context = {
        'PricingCategories': PricingCategories
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
@csrf_exempt
def create_sub(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_method = data['payment_method']
        stripe.api_key = djstripe.settings.djstripe_settings.STRIPE_SECRET_KEY

        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

        try:
            customer = stripe.Customer.create(
                payment_method=payment_method,
                email=request.user.email,
                invoice_settings={
                    'default_payment_method': payment_method
                }
            )
            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)

            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        "price": data["price_id"]
                    }
                ],
                expand=["latest_invoice.payment_intent"]
            )

            djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

            request.user.userprofile.subscription = subscription.id
            request.user.userprofile.save()

            return JsonResponse(subscription)

        except Exception as e:
            return JsonResponse({'error': (e.args[0])}, status=403)
    else:
        return HttpResponse('Request method not allowed')


@login_required
@csrf_exempt
def delete_sub(request):
    if request.method == 'POST':
        plan = request.POST.get('cancel_plan', 'Basic')

        to_change = request.user.userprofile

        to_change.plan = plan
        to_change.save()

        messages.success(request, 'Your Pro Membership has been cancelled ')

        return redirect('settings')

    else:
        return HttpResponse('Request method not allowed')


@login_required
def plans(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'dashboard/plans.html', context)


@login_required
def complete(request):
    return render(request, 'dashboard/complete.html')


@login_required
def individual_priced_item(request, individual_priced_item_id):
    individual_priced_item = PricingCategory.objects.get(pk=individual_priced_item_id)
    # print(individualtestzones)
    context = {
        'individual_priced_item': individual_priced_item
    }
    return render(request, 'dashboard/individual_priced_item.html', context)


@login_required
def individual_priced_item_delete(request, individual_priced_item_id):
    individual_priced_item = PricingCategory.objects.filter(made_by=request.user).get(pk=individual_priced_item_id)
    individual_priced_item.delete()
    messages.success(request, 'The Test has been deleted')

    return redirect('dashboard')


@login_required
def settings(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')

        user = request.user

        if username != request.user.username:
            users = User.objects.filter(username=username)

            if len(users):
                messages.error(request, 'The Username already exists ')
            else:
                user.username = username

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'The changes have been saved ')

        return redirect('settings')

    context = {

    }
    return render(request, 'dashboard/settings.html', context)
