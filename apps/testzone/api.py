from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import TestCategory
from django.contrib import messages


@csrf_exempt
def api_delete_test(request, individualtestzone_id):
    individualtestzone = request.user.TestCategories.all().get(pk=individualtestzone_id)

    individualtestzone.delete()

    return JsonResponse({'success': True})
