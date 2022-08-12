from django.urls import path
from .views import dashboard, individual_priced_item, settings, individual_priced_item_delete, plans, complete, \
    create_sub, delete_sub, more_info_user
from apps.testzone.views import testzone, individualtestzone, testzone_add, testzone_edit, testzone_delete, \
    testzone_chiffrer
from apps.testzone.api import api_delete_test
from apps.files_management.views import file_selector
from apps.resultmanagement.views import inventaire_des_strategies_de_groupe, points_de_controle_ad, rapport_de_conf_ad,\
    rapport_d_inventaire_ad

urlpatterns = [
    path('dashboard/more_info_user/', more_info_user, name='more_info_user'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create-sub/', create_sub, name='create_sub'),
    path('delete-sub/', delete_sub, name='delete_sub'),
    path('dashboard/<int:individual_priced_item_id>/', individual_priced_item, name='individual_priced_item'),
    path('dashboard/<int:individual_priced_item_id>/delete/', individual_priced_item_delete,
         name='individual_priced_item_delete'),

    #path('dashboard/file_upload/', file_selector, name='file_selector'),

    path('settings/', settings, name='settings'),
    path('settings/plans/', plans, name='plans'),
    path('settings/plans/complete', complete, name='complete'),

    path('testzone/', testzone, name='testzone'),
    # path('testzone/add/', testzone_add, name='testzone_add'),
    path('inventaire_des_strategies_de_groupe/', inventaire_des_strategies_de_groupe,
         name='inventaire_des_strategies_de_groupe'),
    path('points_de_controle_ad/', points_de_controle_ad, name='points_de_controle_ad'),
    path('rapport_de_conf_ad/', rapport_de_conf_ad, name='rapport_de_conf_ad'),
    path('rapport_d_inventaire_ad/', rapport_d_inventaire_ad, name='rapport_d_inventaire_ad'),

    # path--

    path('files/file_upload/', file_selector, name='file_selector'),
    path('testzone/<int:individualtestzone_id>/testzone_chiffrer/', testzone_chiffrer, name='testzone_chiffrer'),
    path('testzone/<int:individualtestzone_id>/edit/', testzone_edit, name='testzone_edit'),
    path('testzone/<int:individualtestzone_id>/delete/', testzone_delete, name='testzone_delete'),
    path('testzone/<int:individualtestzone_id>/', individualtestzone, name='individualtestzone'),

    path('api/testzone_delete/<int:individualtestzone_id>/', api_delete_test, name='api_delete_test'),
]

