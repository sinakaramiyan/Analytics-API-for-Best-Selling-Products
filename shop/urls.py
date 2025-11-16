from django.urls import path
from .views import TopTenBestSellerProduct

urlpatterns = [
    path('', TopTenBestSellerProduct.as_view(), name='top-ten-product'),
]
