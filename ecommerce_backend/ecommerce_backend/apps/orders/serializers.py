from rest_framework import serializers
from .models import Order, OrderItem, Payment
from ecommerce_backend.apps.products.serializers import ProductListSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductListSerializer(source='product', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_details', 'product_name', 'product_price', 'quantity', 'total_price')
        read_only_fields = ('product_name', 'product_price', 'total_price')

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('order', 'amount', 'currency')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
    item_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Order
        fields = (
            'id', 'order_number', 'user', 'status', 'payment_status',
            'subtotal', 'tax_amount', 'shipping_cost', 'total_amount',
            'shipping_address', 'shipping_city', 'shipping_state', 
            'shipping_zipcode', 'shipping_country',
            'customer_email', 'customer_phone',
            'items', 'payment', 'item_count',
            'created_at', 'updated_at', 'paid_at', 'shipped_at', 'delivered_at'
        )
        read_only_fields = ('user', 'order_number', 'subtotal', 'tax_amount', 'total_amount')

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)
    
    class Meta:
        model = Order
        fields = (
            'shipping_address', 'shipping_city', 'shipping_state', 
            'shipping_zipcode', 'shipping_country',
            'customer_email', 'customer_phone',
            'items'
        )

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Calculate order totals
        subtotal = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.name}. Available: {product.stock}, Requested: {quantity}"
                )
            
            subtotal += product.price * quantity
        
        # Calculate tax and shipping (simplified)
        tax_amount = subtotal * 0.08  # 8% tax
        shipping_cost = 10.00  # Fixed shipping cost
        
        # Create order
        order = Order.objects.create(
            user=user,
            customer_email=user.email,
            subtotal=subtotal,
            tax_amount=tax_amount,
            shipping_cost=shipping_cost,
            **validated_data
        )
        
        # Create order items and update product stock
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_price=product.price,
                quantity=quantity
            )
            
            # Update product stock
            product.stock -= quantity
            product.save()
        
        return order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('payment_method',)