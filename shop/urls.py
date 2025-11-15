from django.urls import path
from .views import TopTenBestSellerProduct

urlpatterns = [
    path('top-ten-best-sellers/', TopTenBestSellerProduct.as_view(), name='top-ten-product'),
]
