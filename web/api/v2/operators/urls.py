from django.urls import path

from . import operators

urlpatterns = [
    path('upload-xlsx-template', operators.excel_template_upload, name='api-v2-operators-excel-template-upload'),
    path('download-xlsx-template', operators.excel_template_download, name='api-v2-operators-excel-template-download'),

    # get
    path('lots/drafts', operators.get_drafts, name='api-v2-operators-get-drafts'),
    path('lots/in', operators.get_in, name='api-v2-operators-get-in'),
    path('lots/out', operators.get_out, name='api-v2-operators-get-out'),

    # export
    path('lots/drafts/export', operators.export_drafts, name='api-v2-operators-export-drafts'),
    path('lots/in/export', operators.export_in, name='api-v2-operators-export-in'),
    path('lots/out/export', operators.export_out, name='api-v2-operators-export-out'),

    # post
    path('lots/delete', operators.delete_lots, name='api-v2-operators-delete-lots'),
    path('lots/accept', operators.accept_lots, name='api-v2-operators-accept-lots'),
    path('lots/declare', operators.declare_lots, name='api-v2-operators-declare-lots'),
    path('lots/validate', operators.validate_lots, name='api-v2-operators-validate-lots'),


    path('lot/reject', operators.reject_lot, name='api-v2-operators-reject-lot'),
    path('lot/accept', operators.accept_lot, name='api-v2-operators-accept-lot'),
    path('lot/accept-with-correction', operators.accept_lot_with_correction, name='api-v2-operators-accept-lot-with-correction'),
]
