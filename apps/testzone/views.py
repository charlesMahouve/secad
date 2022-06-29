from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import TestCategory

from .forms import CategoryForm


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
        'form': form
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
