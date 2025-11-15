from rest_framework import serializers

# Implement a serializer to return the top ten best-selling products for analytics 
class TopSellingProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_sold = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    order_count = serializers.IntegerField(read_only=True)
    
    def to_representation(self, instance):
        """تبدیل به فرمت مناسب برای نمایش"""
        data = super().to_representation(instance)
        data['price'] = float(data['price'])
        data['total_revenue'] = float(data['total_revenue'])
        return data
