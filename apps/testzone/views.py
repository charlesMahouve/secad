from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import TestCategory

from .forms import CategoryForm
from apps.dashboard.forms import PricingForm


# Create your views here.

@login_required
def testzone(request):
    TestCategories = request.user.TestCategories.all()

    context = {
        'TestCategories': TestCategories
    }
    return render(request, 'bookmark/testzone.html', context)


@login_required
def individualtestzone(request, individualtestzone_id):
    individualtestzones = TestCategory.objects.get(pk=individualtestzone_id)
    # print(individualtestzones)
    # print(individualtestzones.id)
    # individualtestzones = TestCategory.objects.get(pk=individualtestzone_id)

    context = {
        'individualtestzones': individualtestzones
    }
    return render(request, 'bookmark/individualtestzone.html', context)


@login_required
def testzone_add(request):
    canAdd = ''

    testnumbers = request.user.TestCategories.all().count()
    if testnumbers >= 500 and request.user.userprofile.plan == 'pro':
        canAdd = 'You can\'t have more than 5OO tests when you\'re on the Pro plan'
    if testnumbers >= 5 and request.user.userprofile.plan == 'basic':
        canAdd = 'You can\'t have more than 5 tests when you\'re on the basic plan'

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            individualtestzone = form.save(commit=False)
            individualtestzone.run_by = request.user
            individualtestzone.save()

            messages.success(request, 'The Test has been added')

            return redirect('testzone')
    else:
        form = CategoryForm()

    context = {
        'form': form,
        'canAdd': canAdd
    }
    return render(request, 'bookmark/testzone_add.html', context)


@login_required
def testzone_edit(request, individualtestzone_id):
    individualtestzone = TestCategory.objects.filter(run_by=request.user).get(pk=individualtestzone_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=individualtestzone, )

        if form.is_valid():
            form.save()
            messages.success(request, 'The Test has been Updated')

            return redirect('testzone')
    else:
        form = CategoryForm(instance=individualtestzone)

    context = {
        'form': form
    }
    return render(request, 'bookmark/testzone_edit.html', context)


@login_required
def testzone_delete(request, individualtestzone_id):
    individualtestzone = TestCategory.objects.filter(run_by=request.user).get(pk=individualtestzone_id)
    print(individualtestzone)
    individualtestzone.delete()
    messages.success(request, 'The Test has been deleted')

    return redirect('testzone')


@login_required
def testzone_chiffrer(request, individualtestzone_id):
    individualtestzone = TestCategory.objects.filter(run_by=request.user).get(pk=individualtestzone_id)
    if request.method == 'POST':
        form = PricingForm(request.POST)

        if form.is_valid():
            individual_priced_item = form.save(commit=False)
            individual_priced_item.made_by = request.user
            individual_priced_item.save()

            messages.success(request, 'The Money has been added')

            return redirect('dashboard')
    else:
        form = PricingForm()

    context = {
        'form': form,
        'individualtestzone': individualtestzone,
    }
    return render(request, 'bookmark/testzone_chiffrer.html', context)
