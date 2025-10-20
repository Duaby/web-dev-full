from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Subscriber(models.Model):
    """Email subscribers for newsletter"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, db_index=True)
    subscribed_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['-subscribed_at']
        indexes = [
            models.Index(fields=['-subscribed_at'], name='subscriber_date_idx'),
            models.Index(fields=['email', 'is_active'], name='subscriber_email_active_idx'),
        ]
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'

    def __str__(self):
        return f"{self.name} - {self.email}"


class Category(models.Model):
    """Recipe categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'], name='category_name_idx'),
        ]

    def __str__(self):
        return self.name

    def get_recipe_count(self):
        """Get number of recipes in this category"""
        return self.recipes.count()


class Recipe(models.Model):
    """Restaurant recipes - both admin and user submitted"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    APPROVAL_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField()
    ingredients = models.TextField(help_text="One ingredient per line")
    instructions = models.TextField()
    prep_time = models.PositiveIntegerField(
        help_text="Preparation time in minutes",
        validators=[MinValueValidator(1)]
    )
    cook_time = models.PositiveIntegerField(
        help_text="Cooking time in minutes",
        validators=[MinValueValidator(1)]
    )
    servings = models.PositiveIntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(50)]
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium',
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='recipes',
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True
    )
    image_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    
    # NEW: Approval system fields
    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='approved',  # Admin recipes auto-approved
        db_index=True
    )
    is_user_recipe = models.BooleanField(default=False, db_index=True)
    rejection_reason = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_recipes'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'], name='recipe_created_idx'),
            models.Index(fields=['category', '-created_at'], name='recipe_cat_date_idx'),
            models.Index(fields=['is_featured', '-created_at'], name='recipe_featured_idx'),
            models.Index(fields=['difficulty', '-created_at'], name='recipe_diff_date_idx'),
            models.Index(fields=['title'], name='recipe_title_idx'),
            models.Index(fields=['approval_status', '-created_at'], name='recipe_approval_date_idx'),
            models.Index(fields=['is_user_recipe', 'approval_status'], name='recipe_user_approval_idx'),
        ]
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.title

    @property
    def total_time(self):
        """Calculate total cooking time"""
        return self.prep_time + self.cook_time

    def get_average_rating(self):
        """Calculate average rating from approved reviews"""
        approved_reviews = self.reviews.filter(is_approved=True)
        if approved_reviews.exists():
            total = sum(review.rating for review in approved_reviews)
            return round(total / approved_reviews.count(), 1)
        return None

    def get_review_count(self):
        """Get count of approved reviews"""
        return self.reviews.filter(is_approved=True).count()
    
    def get_favorite_count(self):
        """Get number of users who favorited this recipe"""
        return self.favorited_by.count()


class Review(models.Model):
    """Recipe reviews and ratings"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True
    )
    reviewer_name = models.CharField(max_length=100)
    reviewer_email = models.EmailField(db_index=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        db_index=True
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_approved = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['recipe', 'reviewer_email']
        indexes = [
            models.Index(fields=['recipe', 'is_approved'], name='review_recipe_approved_idx'),
            models.Index(fields=['is_approved', '-created_at'], name='review_approved_date_idx'),
            models.Index(fields=['rating', '-created_at'], name='review_rating_date_idx'),
        ]
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.reviewer_name} - {self.recipe.title} ({self.rating}★)"

    def clean(self):
        """Validate review data"""
        from django.core.exceptions import ValidationError
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5')


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_read', '-created_at'], name='contact_read_date_idx'),
            models.Index(fields=['-created_at'], name='contact_created_idx'),
        ]
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.subject}"

    def mark_as_read(self):
        """Mark message as read"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])


class Favorite(models.Model):
    """User favorite recipes"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        unique_together = ['user', 'recipe']
        ordering = ['-created_at']
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
    
    def __str__(self):
        return f"{self.user.username} ❤️ {self.recipe.title}"