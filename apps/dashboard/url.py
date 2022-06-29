from django.urls import path
from .views import dashboard
from apps.testzone.views import testzone, individualtestzone, testzone_add, testzone_edit, testzone_delete
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('testzone/', testzone, name='testzone'),
    path('testzone/add/', testzone_add, name='testzone_add'),
    path('testzone/<int:individualtestzone_id>/edit/', testzone_edit, name='testzone_edit'),
    path('testzone/<int:individualtestzone_id>/delete/', testzone_delete, name='testzone_delete'),
    path('testzone/<int:individualtestzone_id>/', individualtestzone, name='individualtestzone'),
]
