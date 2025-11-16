from rest_framework.views import View, APIView
from .models import Product, Order, Customer
from django.db.models import Sum, Count, F, Q, Avg
from datetime import datetime, timedelta
from rest_framework.response import Response
from .serializers import TopSellingProductSerializer
from utils.decorators import auto_cache
from django.core.cache import cache
import redis 
class TopTenBestSellerProduct(APIView):
    @auto_cache(key_prefix="shop", timeout=3600)
    def get(self, request):

        # time.sleep(2)
        # cache_key = f"shop:{key}"
        cache_key = ''
        # print(cache.)
        top_products = cache.get('shop:shop')

        if top_products is None:
            from_date = datetime.now() - timedelta(days=30)
            
            top_products = Product.objects.filter(
                orderitem__order__order_date__gte=from_date,
                orderitem__order__status__in=['delivered', 'shipped']
            ).annotate(
                total_sold=Sum('orderitem__quantity'),
                total_revenue=Sum(F('orderitem__quantity') * F('orderitem__price')),
                order_count=Count('orderitem__order', distinct=True)
            ).filter(
                total_sold__isnull=False
            ).order_by('-total_sold')[:10]
        
        serializer = TopSellingProductSerializer(top_products, many=True)

        return Response(serializer.data)
