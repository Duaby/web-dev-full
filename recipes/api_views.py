from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscriber, Category, Recipe, Review, ContactMessage
from .serializers import (
    SubscriberSerializer, CategorySerializer, RecipeListSerializer,
    RecipeDetailSerializer, ReviewSerializer, ContactMessageSerializer,
    RecipeCreateUpdateSerializer
)

# Custom Pagination
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ===== SUBSCRIBER ENDPOINTS =====
class SubscriberListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all subscribers
    POST: Create new subscriber and send welcome email
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['subscribed_at', 'name']

    def perform_create(self, serializer):
        subscriber = serializer.save()
        # Send welcome email with recipe
        self.send_welcome_email(subscriber)

    def send_welcome_email(self, subscriber):
        subject = "Welcome to Our Restaurant Newsletter!"
        message = f"""
        Hi {subscriber.name},

        Thank you for subscribing to our newsletter!

        Here's your first recipe:

        PASTA CARBONARA
        ================
        Ingredients:
        - 400g spaghetti
        - 200g pancetta
        - 4 egg yolks
        - 100g Pecorino Romano
        - Black pepper

        Instructions:
        1. Cook pasta in salted boiling water
        2. Fry pancetta until crispy
        3. Mix egg yolks with grated cheese
        4. Combine everything off heat
        5. Season with black pepper

        Best regards,
        The Restaurant Team
        """
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")


class SubscriberRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve single subscriber
    PUT/PATCH: Update subscriber
    DELETE: Delete subscriber
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    lookup_field = 'pk'


# ===== CATEGORY ENDPOINTS =====
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all categories
    POST: Create new category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve single category
    PUT/PATCH: Update category
    DELETE: Delete category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


# ===== RECIPE ENDPOINTS =====
class RecipeListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all recipes (with filtering, search, ordering)
    POST: Create new recipe
    """
    queryset = Recipe.objects.all()
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'is_featured']
    search_fields = ['title', 'description', 'ingredients']
    ordering_fields = ['created_at', 'title', 'prep_time', 'cook_time']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateUpdateSerializer
        return RecipeListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user if self.request.user.is_authenticated else None)


class RecipeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve single recipe with full details
    PUT/PATCH: Update recipe
    DELETE: Delete recipe
    """
    queryset = Recipe.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RecipeCreateUpdateSerializer
        return RecipeDetailSerializer


@api_view(['GET'])
def featured_recipes(request):
    """Get all featured recipes"""
    recipes = Recipe.objects.filter(is_featured=True)[:6]
    serializer = RecipeListSerializer(recipes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recipe_by_category(request, slug):
    """Get all recipes in a specific category"""
    try:
        category = Category.objects.get(slug=slug)
        recipes = Recipe.objects.filter(category=category)
        paginator = StandardResultsPagination()
        result_page = paginator.paginate_queryset(recipes, request)
        serializer = RecipeListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"},
            status=status.HTTP_404_NOT_FOUND
        )


# ===== REVIEW ENDPOINTS =====
class ReviewListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all reviews
    POST: Create new review
    """
    queryset = Review.objects.filter(is_approved=True)
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['recipe', 'rating']
    ordering_fields = ['created_at', 'rating']


class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve single review
    PUT/PATCH: Update review
    DELETE: Delete review
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'pk'


@api_view(['GET'])
def recipe_reviews(request, recipe_slug):
    """Get all approved reviews for a specific recipe"""
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
        reviews = Review.objects.filter(recipe=recipe, is_approved=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Recipe.DoesNotExist:
        return Response(
            {"error": "Recipe not found"},
            status=status.HTTP_404_NOT_FOUND
        )


# ===== CONTACT MESSAGE ENDPOINTS =====
class ContactMessageListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all contact messages
    POST: Submit new contact message
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'is_read']


class ContactMessageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve single contact message
    PUT/PATCH: Update message (e.g., mark as read)
    DELETE: Delete message
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    lookup_field = 'pk'


# ===== STATISTICS ENDPOINT =====
@api_view(['GET'])
def api_statistics(request):
    """Get overall API statistics"""
    stats = {
        'total_subscribers': Subscriber.objects.filter(is_active=True).count(),
        'total_recipes': Recipe.objects.count(),
        'total_categories': Category.objects.count(),
        'total_reviews': Review.objects.filter(is_approved=True).count(),
        'featured_recipes': Recipe.objects.filter(is_featured=True).count(),
        'pending_reviews': Review.objects.filter(is_approved=False).count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
    }
    return Response(stats)
