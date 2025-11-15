from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Customer, Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'orders_count', 'created_at')
    
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'orders_count')
    
    def orders_count(self, obj):
        return obj.orderitem_set.count()
    orders_count.short_description = 'Times Ordered'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'status', 'total_amount', 'items_count')
    list_filter = ('status', 'order_date')
    search_fields = ('customer__user__username', 'customer__user__first_name', 'customer__user__last_name')
    readonly_fields = ('order_date', 'total_amount', 'items_count')
    list_editable = ('status',)
    
    def items_count(self, obj):
        return obj.orderitem_set.count()
    items_count.short_description = 'Items Count'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer__user').prefetch_related('orderitem_set')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'get_item_total')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('get_item_total',)
    
    def get_item_total(self, obj):
        return f"${obj.get_item_total():.2f}"
    get_item_total.short_description = 'Item Total'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'product', 'order__customer__user')


admin.site.site_header = "Shop Administration"
admin.site.site_title = "Shop Admin Portal"
admin.site.index_title = "Welcome to Shop Admin Portal"