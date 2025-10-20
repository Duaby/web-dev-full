from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User Dashboard & Profile
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # Recipe Management
    path('submit-recipe/', views.submit_recipe_view, name='submit_recipe'),
    path('recipe/edit/<slug:slug>/', views.edit_recipe_view, name='edit_recipe'),
    path('recipe/delete/<slug:slug>/', views.delete_recipe_view, name='delete_recipe'),
    
    # Favorites
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorite/toggle/<int:recipe_id>/', views.toggle_favorite_view, name='toggle_favorite'),
    
    # Public Pages
    path('guest-recipes/', views.guest_recipes_view, name='guest_recipes'),
    path('recipe/<slug:slug>/', views.recipe_detail_view, name='recipe_detail'),
]