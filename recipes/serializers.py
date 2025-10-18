from rest_framework import serializers
from .models import Subscriber, Category, Recipe, Review, ContactMessage
from django.contrib.auth.models import User

class SubscriberSerializer(serializers.ModelSerializer):
    """Serializer for email subscribers"""
    class Meta:
        model = Subscriber
        fields = ['id', 'name', 'email', 'subscribed_at', 'is_active']
        read_only_fields = ['id', 'subscribed_at']

    def validate_email(self, value):
        if self.instance is None:  # Only check on creation
            if Subscriber.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already subscribed.")
        return value.lower()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for recipe categories"""
    recipe_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'recipe_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_recipe_count(self, obj):
        return obj.recipes.count()


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for recipe reviews"""
    recipe_title = serializers.CharField(source='recipe.title', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'recipe', 'recipe_title', 'reviewer_name', 'reviewer_email',
                  'rating', 'comment', 'created_at', 'is_approved']
        read_only_fields = ['id', 'created_at', 'is_approved']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class RecipeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for recipe listings"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'slug', 'description', 'category_name',
                  'author_name', 'difficulty', 'total_time', 'servings',
                  'image_url', 'is_featured', 'average_rating', 'review_count',
                  'created_at']

    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single recipe view"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author_name = serializers.CharField(source='author.username', read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    ingredients_list = serializers.SerializerMethodField()
    instructions_list = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'slug', 'description', 'ingredients', 'ingredients_list',
                  'instructions', 'instructions_list', 'prep_time', 'cook_time',
                  'total_time', 'servings', 'difficulty', 'category', 'category_name',
                  'author', 'author_name', 'image_url', 'is_featured', 'reviews',
                  'average_rating', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_time']

    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    def get_ingredients_list(self, obj):
        return [line.strip() for line in obj.ingredients.split('\n') if line.strip()]

    def get_instructions_list(self, obj):
        return [line.strip() for line in obj.instructions.split('\n') if line.strip()]


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for contact form messages"""
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at', 'is_read']
        read_only_fields = ['id', 'created_at', 'is_read']

    def validate_message(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long.")
        return value


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating recipes"""
    class Meta:
        model = Recipe
        fields = ['title', 'slug', 'description', 'ingredients', 'instructions',
                  'prep_time', 'cook_time', 'servings', 'difficulty', 'category',
                  'image_url', 'is_featured']

    def validate_slug(self, value):
        if self.instance:  # Update case
            if Recipe.objects.exclude(pk=self.instance.pk).filter(slug=value).exists():
                raise serializers.ValidationError("A recipe with this slug already exists.")
        else:  # Create case
            if Recipe.objects.filter(slug=value).exists():
                raise serializers.ValidationError("A recipe with this slug already exists.")
        return value
