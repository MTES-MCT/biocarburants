from django.urls import path
from . import views

urlpatterns = [
    # GET
    path('', views.get_lots, name='api-v3-lots-get'),
    path('details', views.get_details, name='api-v3-lots-get-details'),
    path('snapshot', views.get_snapshot, name='api-v3-lots-get-snapshot'),
    path('filters', views.get_filters, name='api-v3-lots-get-filters'),
    path('declaration-summary', views.get_declaration_summary, name='api-v3-lots-get-declaration-summary'),
    path('summary', views.get_lots_summary, name='api-v3-lots-get-lots-summary'),

    # POST
    path('add', views.add_lot, name='api-v3-add-lot'),
    path('update', views.update_lot, name='api-v3-update-lot'),
    path('delete', views.delete_lot, name='api-v3-delete-lot'),
    path('duplicate', views.duplicate_lot, name='api-v3-duplicate-lot'),
    path('validate', views.validate_lot, name='api-v3-validate-lot'),
    path('accept', views.accept_lot, name='api-v3-accept-lot'),
    path('accept-with-reserves', views.accept_with_reserves, name='api-v3-accept-lot-with-reserves'),
    path('amend-lot', views.amend_lot, name='api-v3-amend-lot'),
    path('reject', views.reject_lot, name='api-v3-reject-lot'),
    path('comment', views.comment_lot, name='api-v3-comment-lot'),


    # DECLARATION
    path('validate-declaration', views.validate_declaration, name='api-v3-validate-declaration'),


    # SPECIAL
    path('forward', views.forward_lots, name='api-v3-forward-lot'),


    # IMPORT/FILES
    path('upload', views.upload, name='api-v3-upload'),
    path('upload-blend', views.upload_blend, name='api-v3-upload-blend'),

    path('download-template-simple', views.get_template_producers_simple, name='api-v3-template-simple'),
    path('download-template-advanced', views.get_template_producers_advanced, name='api-v3-template-advanced'),
    path('download-template-advanced-10k', views.get_template_producers_advanced_10k, name='api-v3-template-advanced-10k'),
    path('download-template-blend', views.get_template_blend, name='api-v3-template-blend'),
    path('download-template-trader', views.get_template_trader, name='api-v3-template-trader'),
]
