from django.contrib import admin
from .models import Order, OrderItem, Payment

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price', 'total_price')

class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    readonly_fields = ('payment_id', 'amount', 'currency')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'user__email', 'customer_email')
    readonly_fields = ('order_number', 'subtotal', 'tax_amount', 'total_amount')
    inlines = [OrderItemInline, PaymentInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'tax_amount', 'shipping_cost', 'total_amount')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country')
        }),
        ('Customer Information', {
            'fields': ('customer_email', 'customer_phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'paid_at', 'shipped_at', 'delivered_at')
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'payment_method', 'amount', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('order__order_number', 'payment_id')
    readonly_fields = ('payment_id', 'amount', 'currency')

admin.site.register(OrderItem)
