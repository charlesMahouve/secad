from django.urls import path
from .views import dashboard, individual_priced_item, settings, individual_priced_item_delete, plans, complete, \
    create_sub
from apps.testzone.views import testzone, individualtestzone, testzone_add, testzone_edit, testzone_delete, \
    testzone_chiffrer
from apps.testzone.api import api_delete_test

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('create-sub/', create_sub, name='create_sub'),
    path('dashboard/<int:individual_priced_item_id>/', individual_priced_item, name='individual_priced_item'),
    path('dashboard/<int:individual_priced_item_id>/delete/', individual_priced_item_delete,
         name='individual_priced_item_delete'),
    path('settings/', settings, name='settings'),
    path('settings/plans/', plans, name='plans'),
    path('settings/plans/complete', complete, name='complete'),

    path('testzone/', testzone, name='testzone'),
    path('testzone/add/', testzone_add, name='testzone_add'),
    path('testzone/<int:individualtestzone_id>/testzone_chiffrer/', testzone_chiffrer, name='testzone_chiffrer'),
    path('testzone/<int:individualtestzone_id>/edit/', testzone_edit, name='testzone_edit'),
    path('testzone/<int:individualtestzone_id>/delete/', testzone_delete, name='testzone_delete'),
    path('testzone/<int:individualtestzone_id>/', individualtestzone, name='individualtestzone'),

    path('api/testzone_delete/<int:individualtestzone_id>/', api_delete_test, name='api_delete_test'),
]
