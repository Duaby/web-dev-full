from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg, Count, Q
from .models import Subscriber, Category, Recipe, Review, ContactMessage
from .serializers import (
    SubscriberSerializer, CategorySerializer, RecipeListSerializer,
    RecipeDetailSerializer, ReviewSerializer, ContactMessageSerializer,
    RecipeCreateUpdateSerializer
)
from .permissions import IsAdminOrReadOnly, IsAuthenticatedOrPostOnly
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Custom Pagination
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ===== SUBSCRIBER ENDPOINTS =====
class SubscriberListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all subscribers (Admin only)
    POST: Create new subscriber and send welcome email (Public)
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['subscribed_at', 'name']
    ordering = ['-subscribed_at']
    permission_classes = [IsAuthenticatedOrPostOnly]  # ADDED

    def get_queryset(self):
        """Admin sees all, others see nothing on GET"""
        if self.request.method == 'GET':
            if self.request.user and self.request.user.is_staff:
                return Subscriber.objects.all()
            return Subscriber.objects.none()
        return Subscriber.objects.all()

    def perform_create(self, serializer):
        subscriber = serializer.save()
        try:
            self.send_welcome_email(subscriber)
        except Exception as e:
            logger.error(f"Failed to send welcome email to {subscriber.email}: {e}")

    def send_welcome_email(self, subscriber):
        """Send welcome email with recipe"""
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
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [subscriber.email],
            fail_silently=True,
        )


class SubscriberRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/PATCH/DELETE: Subscriber operations (Admin only)
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminOrReadOnly]  # ADDED


# ===== CATEGORY ENDPOINTS =====
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all categories (Public)
    POST: Create new category (Admin only)
    """
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    permission_classes = [IsAdminOrReadOnly]  # ADDED
    
    def get_queryset(self):
        return Category.objects.annotate(
            recipe_count=Count('recipes')
        )


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve single category (Public)
    PUT/PATCH/DELETE: Update/delete category (Admin only)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]  # ADDED


# ===== RECIPE ENDPOINTS =====
class RecipeListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all recipes (Public)
    POST: Create new recipe (Admin only)
    """
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'is_featured']
    search_fields = ['title', 'description', 'ingredients']
    ordering_fields = ['created_at', 'title', 'prep_time', 'cook_time']
    ordering = ['-created_at']
    permission_classes = [IsAdminOrReadOnly]  # ADDED

    def get_queryset(self):
        return Recipe.objects.select_related(
            'category', 'author'
        ).prefetch_related(
            'reviews'
        ).annotate(
            avg_rating=Avg('reviews__rating', filter=Q(reviews__is_approved=True)),
            review_count=Count('reviews', filter=Q(reviews__is_approved=True))
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateUpdateSerializer
        return RecipeListSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user if self.request.user.is_authenticated else None
        )


class RecipeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve single recipe (Public)
    PUT/PATCH/DELETE: Update/delete recipe (Admin only)
    """
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]  # ADDED
    
    def get_queryset(self):
        return Recipe.objects.select_related(
            'category', 'author'
        ).prefetch_related(
            'reviews'
        )

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RecipeCreateUpdateSerializer
        return RecipeDetailSerializer


@api_view(['GET'])
@permission_classes([AllowAny])  # ADDED
def featured_recipes(request):
    """Get all featured recipes (Public)"""
    recipes = Recipe.objects.filter(
        is_featured=True
    ).select_related(
        'category', 'author'
    ).prefetch_related(
        'reviews'
    )[:6]
    
    serializer = RecipeListSerializer(recipes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])  # ADDED
def recipe_by_category(request, slug):
    """Get all recipes in a specific category (Public)"""
    try:
        category = Category.objects.get(slug=slug)
        recipes = Recipe.objects.filter(
            category=category
        ).select_related(
            'category', 'author'
        ).prefetch_related(
            'reviews'
        )
        
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
    GET: List all approved reviews (Public)
    POST: Create new review (Public)
    """
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['recipe', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    permission_classes = [AllowAny]  # ADDED - Allow anyone to submit reviews
    
    def get_queryset(self):
        # Only show approved reviews to public
        if self.request.user and self.request.user.is_staff:
            return Review.objects.select_related('recipe')
        return Review.objects.filter(
            is_approved=True
        ).select_related('recipe')


class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve single review (Public if approved)
    PUT/PATCH/DELETE: Update/delete review (Admin only)
    """
    queryset = Review.objects.select_related('recipe')
    serializer_class = ReviewSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminOrReadOnly]  # ADDED


@api_view(['GET'])
@permission_classes([AllowAny])  # ADDED
def recipe_reviews(request, recipe_slug):
    """Get all approved reviews for a specific recipe (Public)"""
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
        reviews = Review.objects.filter(
            recipe=recipe,
            is_approved=True
        ).select_related('recipe')
        
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
    GET: List all contact messages (Admin only)
    POST: Submit new contact message (Public)
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_read']
    ordering_fields = ['created_at', 'is_read']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticatedOrPostOnly]  # ADDED

    def get_queryset(self):
        """Admin sees all, others see nothing on GET"""
        if self.request.method == 'GET':
            if self.request.user and self.request.user.is_staff:
                return ContactMessage.objects.all()
            return ContactMessage.objects.none()
        return ContactMessage.objects.all()


class ContactMessageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/PATCH/DELETE: Contact message operations (Admin only)
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminOrReadOnly]  # ADDED


# ===== STATISTICS ENDPOINT =====
@api_view(['GET'])
@permission_classes([AllowAny])  # ADDED
def api_statistics(request):
    """Get overall API statistics (Public)"""
    stats = {
        'total_subscribers': Subscriber.objects.filter(is_active=True).count(),
        'total_recipes': Recipe.objects.count(),
        'total_categories': Category.objects.count(),
        'total_reviews': Review.objects.filter(is_approved=True).count(),
        'featured_recipes': Recipe.objects.filter(is_featured=True).count(),
    }
    
    # Add admin-only stats
    if request.user and request.user.is_staff:
        stats.update({
            'pending_reviews': Review.objects.filter(is_approved=False).count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        })
    
    return Response(stats)


# ===== SEARCH ENDPOINT =====
@api_view(['GET'])
@permission_classes([AllowAny])  # ADDED
def global_search(request):
    """
    Global search across recipes and categories (Public)
    Query parameter: ?q=search_term
    """
    query = request.GET.get('q', '').strip()
    
    if not query:
        return Response(
            {"error": "Search query parameter 'q' is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Search in recipes
    recipes = Recipe.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(ingredients__icontains=query)
    ).select_related('category', 'author')[:10]
    
    # Search in categories
    categories = Category.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )[:5]
    
    results = {
        'recipes': RecipeListSerializer(recipes, many=True).data,
        'categories': CategorySerializer(categories, many=True).data,
        'total_results': recipes.count() + categories.count()
    }
    
    return Response(results)