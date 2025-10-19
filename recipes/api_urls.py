from django.urls import path
from .api_views import (
    # Subscriber views
    SubscriberListCreateAPIView,
    SubscriberRetrieveUpdateDestroyAPIView,
    
    # Category views
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
    
    # Recipe views
    RecipeListCreateAPIView,
    RecipeRetrieveUpdateDestroyAPIView,
    featured_recipes,
    recipe_by_category,
    
    # Review views
    ReviewListCreateAPIView,
    ReviewRetrieveUpdateDestroyAPIView,
    recipe_reviews,
    
    # Contact views
    ContactMessageListCreateAPIView,
    ContactMessageRetrieveUpdateDestroyAPIView,
    
    # Statistics and Search
    api_statistics,
    global_search,  # ADDED - New global search endpoint
)

app_name = 'api'

urlpatterns = [
    # ===== API ROOT =====
    path('', api_statistics, name='api-root'),  # ADDED - Shows stats at /api/
    
    # ===== SUBSCRIBER ENDPOINTS =====
    path('subscribers/', SubscriberListCreateAPIView.as_view(), name='subscriber-list'),
    path('subscribers/<int:pk>/', SubscriberRetrieveUpdateDestroyAPIView.as_view(), name='subscriber-detail'),
    
    # ===== CATEGORY ENDPOINTS =====
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
    path('categories/<slug:slug>/recipes/', recipe_by_category, name='category-recipes'),
    
    # ===== RECIPE ENDPOINTS =====
    path('recipes/', RecipeListCreateAPIView.as_view(), name='recipe-list'),
    path('recipes/featured/', featured_recipes, name='recipe-featured'),
    path('recipes/<slug:slug>/', RecipeRetrieveUpdateDestroyAPIView.as_view(), name='recipe-detail'),
    path('recipes/<slug:recipe_slug>/reviews/', recipe_reviews, name='recipe-reviews'),
    
    # ===== REVIEW ENDPOINTS =====
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-detail'),
    
    # ===== CONTACT MESSAGE ENDPOINTS =====
    path('contact/', ContactMessageListCreateAPIView.as_view(), name='contact-list'),
    path('contact/<int:pk>/', ContactMessageRetrieveUpdateDestroyAPIView.as_view(), name='contact-detail'),
    
    # ===== UTILITIES =====
    path('stats/', api_statistics, name='api-stats'),
    path('search/', global_search, name='global-search'),  # ADDED - Global search
]