from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/export/csv/', views.products_report_csv, name='products_report_csv'),
    path('products/upload/csv/', views.upload_csv, name='upload_csv'),
    path('products/download/csv/', views.download_csv_example, name='download_csv_example'),
    path('product/add/', views.product_create, name='product_create'),
    path('product/edit/<pk>/', views.product_update, name='product_update'),
    path('product/bling_update/<pk>/', views.product_update_from_bling, name='bling_update'),
    path('notas/', views.nota_list, name='nota_list'),
    path('nota/add/', views.nota_create, name='nota_create'),
    path('nota/edit/<pk>/', views.nota_update, name='nota_update'),
    path('nota/copy/<pk>/', views.nota_copy, name='nota_copy'),
    path('nota/export/csv/<pk>/', views.nota_export_csv, name='nota_export_csv'),
    path('nota/export/xls/<pk>/', views.nota_export_xls, name='nota_export_xls'),
    path('nota/export/xlsx/<pk>/', views.nota_export_xlsx, name='nota_export_xlsx'),
    path('nota/export/pdf/<pk>/', views.nota_export_pdf, name='nota_export_pdf'),
    path('nota/export/ci/<pk>/', views.nota_export_commercial_invoice, name='nota_export_ci'),
]
