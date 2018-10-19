from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('product/add/', views.product_create, name='product_create'),
    path('notas/', views.nota_list, name='nota_list'),
]
