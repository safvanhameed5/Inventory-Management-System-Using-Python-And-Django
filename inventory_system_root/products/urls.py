from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.list_products),
    path('products/<pk>/', views.create_product, name='update'),
    path('create-product/', views.create_product),
    path('delete-product/', views.delete_product),
    path('update-product/', views.update_product),
    #path('home/', views.home),
]