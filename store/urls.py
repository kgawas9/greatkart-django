from django.urls import path
from . import views

urlpatterns = [
    path('', views.storeHomePage, name='storePage'),
    path('<slug:category_slug>/', views.storeHomePage, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>', views.product_detail, name='product_detail'),
]