from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('product/add/', views.product_create, name='product_create'),
    path('product/edit/<pk>/', views.product_update, name='product_update'),
    path('notas/', views.nota_list, name='nota_list'),
    path('notas/add/', views.nota_create, name='nota_create'),
    path('nota/edit/<pk>/', views.nota_update, name='nota_update'),
    path('nota/export/csv/<pk>/', views.nota_export_csv, name='nota_export_csv'),
    # path('notas/cbv/', views.NotaView.as_view(), name='nota_cbv'),
    # path('notas/edit/<pk>', views.NotaEdit.as_view(), name='nota_edit'),
]
