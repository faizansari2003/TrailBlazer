from django.urls import path
from . import views
from .views import index_view



urlpatterns = [
    path('', index_view, name='index'),
    
    # URL for the "all products" page (may also show bikes depending on the filter).
    path('all-products/', views.all_bikes_view, name='all_products'),
    path('product/product/<int:product_id>/', views.product_detail, name='product'),
    path('search/', views.search_product, name='search_product'),



    # Add any other paths for other views as needed
]