from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Order, Payment
from .serializers import (
    OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer,
    PaymentSerializer, PaymentCreateSerializer
)
from .filters import OrderFilter

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items', 'payment')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'update_status':
            return OrderStatusUpdateSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            order = serializer.save()
            response_serializer = OrderSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update order status (for admin users or specific workflows)"""
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Add any status transition logic here
        serializer.save()
        return Response(OrderSerializer(order).data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        
        if order.status in ['shipped', 'delivered']:
            return Response(
                {'error': 'Cannot cancel order that has already been shipped or delivered.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save()
        
        # Restore product stock
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
        
        return Response(OrderSerializer(order).data)
    
    @action(detail=True, methods=['post'])
    def create_payment(self, request, pk=None):
        """Create payment for an order"""
        order = self.get_object()
        
        if order.payment_status == 'paid':
            return Response(
                {'error': 'Order has already been paid.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment_serializer = PaymentCreateSerializer(data=request.data)
        payment_serializer.is_valid(raise_exception=True)
        
        # In a real application, integrate with payment gateway here
        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            **payment_serializer.validated_data
        )
        
        # Simulate payment processing
        payment.status = 'paid'
        payment.save()
        
        # Update order status
        order.payment_status = 'paid'
        order.paid_at = timezone.now()
        order.save()
        
        return Response(PaymentSerializer(payment).data)

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user).select_related('order')