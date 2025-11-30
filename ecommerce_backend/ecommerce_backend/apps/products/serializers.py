from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductReview

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'alt_text', 'is_primary')

class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = ('id', 'user', 'user_name', 'rating', 'title', 'comment', 'created_at')
        read_only_fields = ('user',)

class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    discount_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'price', 'compare_price', 'discount_percentage', 
                 'category', 'category_name', 'sku', 'stock', 'in_stock', 'primary_image')

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        return None

class ProductDetailSerializer(ProductListSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + (
            'description', 'images', 'reviews', 'average_rating', 'review_count', 
            'created_at', 'updated_at'
        )

    def get_average_rating(self, obj):
        approved_reviews = obj.reviews.filter(is_approved=True)
        if approved_reviews:
            return round(sum(review.rating for review in approved_reviews) / approved_reviews.count(), 1)
        return 0

    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()