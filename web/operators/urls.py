from django.urls import path

from . import views

urlpatterns = [
    path('', views.operators_index, name='operators-index'),
    path('declaration', views.operators_declaration, name='operators-declaration'),
    path('annuaire', views.operators_annuaire, name='operators-annuaire'),
    path('new', views.operators_new_lots, name='operators-new-lots'),
    path('pending', views.operators_pending_lots, name='operators-pending-lots'),
    path('controles', views.operators_controles, name='operators-controles'),
    path('settings', views.operators_settings, name='operators-settings'),
]
