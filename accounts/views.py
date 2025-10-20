from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.utils.text import slugify
from .forms import SignUpForm, LoginForm, UserProfileForm
from .models import UserProfile
from recipes.models import Recipe, Favorite, Category
from recipes.forms import ReviewForm

def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
            return redirect('accounts:dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_url = request.GET.get('next', 'accounts:dashboard')
                return redirect(next_url)
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('recipes:landing_page')


@login_required
def dashboard_view(request):
    """User dashboard with recipe stats and recent activity"""
    user = request.user
    
    # Get user's recipes with stats
    user_recipes = Recipe.objects.filter(author=user).annotate(
        avg_rating=Avg('reviews__rating', filter=Q(reviews__is_approved=True)),
        review_count=Count('reviews', filter=Q(reviews__is_approved=True)),
        favorite_count=Count('favorited_by')
    ).order_by('-created_at')
    
    # Stats by approval status
    stats = {
        'total': user_recipes.count(),
        'pending': user_recipes.filter(approval_status='pending').count(),
        'approved': user_recipes.filter(approval_status='approved').count(),
        'rejected': user_recipes.filter(approval_status='rejected').count(),
        'draft': user_recipes.filter(approval_status='draft').count(),
    }
    
    # Get favorites
    favorites = Favorite.objects.filter(user=user).select_related(
        'recipe', 'recipe__category', 'recipe__author'
    ).order_by('-created_at')[:6]
    
    context = {
        'recipes': user_recipes[:10],  # Recent 10 recipes
        'stats': stats,
        'favorites': favorites,
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_view(request):
    """User profile view and edit"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    # Update stats
    profile.update_recipe_stats()
    
    context = {
        'form': form,
        'profile': profile,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def submit_recipe_view(request):
    """User recipe submission form"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        prep_time = request.POST.get('prep_time')
        cook_time = request.POST.get('cook_time')
        servings = request.POST.get('servings')
        difficulty = request.POST.get('difficulty')
        category_id = request.POST.get('category')
        image_url = request.POST.get('image_url')
        
        # Generate unique slug
        slug = slugify(title)
        original_slug = slug
        counter = 1
        while Recipe.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        try:
            category = Category.objects.get(id=category_id)
            
            recipe = Recipe.objects.create(
                title=title,
                slug=slug,
                description=description,
                ingredients=ingredients,
                instructions=instructions,
                prep_time=int(prep_time),
                cook_time=int(cook_time),
                servings=int(servings),
                difficulty=difficulty,
                category=category,
                author=request.user,
                image_url=image_url if image_url else None,
                approval_status='pending',  # Requires approval
                is_user_recipe=True,
                is_featured=False
            )
            
            # Update user stats
            request.user.profile.update_recipe_stats()
            
            messages.success(request, 'Your recipe has been submitted and is pending approval!')
            return redirect('accounts:dashboard')
        
        except Exception as e:
            messages.error(request, f'Error submitting recipe: {str(e)}')
    
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories,
    }
    
    return render(request, 'accounts/submit_recipe.html', context)


@login_required
def edit_recipe_view(request, slug):
    """Edit user's own recipe"""
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)
    
    if request.method == 'POST':
        recipe.title = request.POST.get('title')
        recipe.description = request.POST.get('description')
        recipe.ingredients = request.POST.get('ingredients')
        recipe.instructions = request.POST.get('instructions')
        recipe.prep_time = int(request.POST.get('prep_time'))
        recipe.cook_time = int(request.POST.get('cook_time'))
        recipe.servings = int(request.POST.get('servings'))
        recipe.difficulty = request.POST.get('difficulty')
        recipe.category_id = request.POST.get('category')
        recipe.image_url = request.POST.get('image_url') or None
        
        # Reset approval status to pending if recipe was rejected
        if recipe.approval_status == 'rejected':
            recipe.approval_status = 'pending'
            recipe.rejection_reason = None
        
        recipe.save()
        
        messages.success(request, 'Your recipe has been updated!')
        return redirect('accounts:dashboard')
    
    categories = Category.objects.all().order_by('name')
    context = {
        'recipe': recipe,
        'categories': categories,
    }
    
    return render(request, 'accounts/edit_recipe.html', context)


@login_required
def delete_recipe_view(request, slug):
    """Delete user's own recipe"""
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)
    
    if request.method == 'POST':
        recipe_title = recipe.title
        recipe.delete()
        messages.success(request, f'Recipe "{recipe_title}" has been deleted.')
        return redirect('accounts:dashboard')
    
    return render(request, 'accounts/delete_recipe.html', {'recipe': recipe})


@login_required
def toggle_favorite_view(request, recipe_id):
    """Toggle favorite status for a recipe"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        recipe=recipe
    )
    
    if not created:
        favorite.delete()
        messages.success(request, f'Removed "{recipe.title}" from favorites.')
    else:
        messages.success(request, f'Added "{recipe.title}" to favorites!')
    
    # Redirect back to the previous page
    return redirect(request.META.get('HTTP_REFERER', 'accounts:dashboard'))


@login_required
def favorites_view(request):
    """View all user favorites"""
    favorites = Favorite.objects.filter(user=request.user).select_related(
        'recipe', 'recipe__category', 'recipe__author'
    ).annotate(
        avg_rating=Avg('recipe__reviews__rating', filter=Q(recipe__reviews__is_approved=True)),
        review_count=Count('recipe__reviews', filter=Q(recipe__reviews__is_approved=True))
    ).order_by('-created_at')
    
    context = {
        'favorites': favorites,
    }
    
    return render(request, 'accounts/favorites.html', context)


def guest_recipes_view(request):
    """Public page showing all approved user-submitted recipes"""
    recipes = Recipe.objects.filter(
        is_user_recipe=True,
        approval_status='approved'
    ).select_related(
        'category', 'author'
    ).annotate(
        avg_rating=Avg('reviews__rating', filter=Q(reviews__is_approved=True)),
        review_count=Count('reviews', filter=Q(reviews__is_approved=True)),
        favorite_count=Count('favorited_by')
    ).order_by('-created_at')
    
    # Filtering
    category_slug = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    search = request.GET.get('search')
    
    if category_slug:
        recipes = recipes.filter(category__slug=category_slug)
    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)
    if search:
        recipes = recipes.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(ingredients__icontains=search)
        )
    
    categories = Category.objects.all().order_by('name')
    
    context = {
        'recipes': recipes,
        'categories': categories,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'search_query': search,
    }
    
    return render(request, 'accounts/guest_recipes.html', context)


def recipe_detail_view(request, slug):
    """Detailed view of a single recipe"""
    recipe = get_object_or_404(
        Recipe.objects.select_related('category', 'author').prefetch_related('reviews'),
        slug=slug
    )
    
    # Check if user has favorited this recipe
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    
    # Get approved reviews
    reviews = recipe.reviews.filter(is_approved=True).order_by('-created_at')
    
    context = {
        'recipe': recipe,
        'is_favorited': is_favorited,
        'reviews': reviews,
    }
    
    return render(request, 'accounts/recipe_detail.html', context)
