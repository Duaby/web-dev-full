from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import UserProfile
from recipes.models import Recipe, Favorite

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipes_submitted', 'recipes_approved', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    list_filter = ['created_at', 'email_notifications']
    readonly_fields = ['created_at', 'updated_at', 'recipes_submitted', 'recipes_approved']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'bio', 'location', 'website', 'avatar_url')
        }),
        ('Statistics', {
            'fields': ('recipes_submitted', 'recipes_approved')
        }),
        ('Preferences', {
            'fields': ('email_notifications',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Update Recipe Admin with approval workflow
@admin.register(Recipe)
class RecipeAdminEnhanced(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'category', 'approval_status_badge', 'is_user_recipe', 'created_at']
    list_filter = ['approval_status', 'is_user_recipe', 'category', 'difficulty', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'ingredients', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'reviewed_by', 'reviewed_at']
    actions = ['approve_recipes', 'reject_recipes', 'mark_as_pending']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'category', 'author')
        }),
        ('Recipe Details', {
            'fields': ('ingredients', 'instructions', 'prep_time', 'cook_time', 'servings', 'difficulty')
        }),
        ('Media & Status', {
            'fields': ('image_url', 'is_featured')
        }),
        ('Approval System', {
            'fields': ('approval_status', 'is_user_recipe', 'rejection_reason', 'reviewed_by', 'reviewed_at'),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def author_name(self, obj):
        return obj.author.get_full_name() if obj.author else 'N/A'
    author_name.short_description = 'Author'
    
    def approval_status_badge(self, obj):
        colors = {
            'approved': '#28a745',
            'pending': '#ffc107',
            'rejected': '#dc3545',
            'draft': '#6c757d'
        }
        color = colors.get(obj.approval_status, '#6c757d')
        return format_html(
            '{}',
            color,
            obj.get_approval_status_display()
        )
    approval_status_badge.short_description = 'Status'
    
    def approve_recipes(self, request, queryset):
        """Approve selected recipes"""
        updated = queryset.update(
            approval_status='approved',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'{updated} recipe(s) approved successfully.')
    approve_recipes.short_description = "✅ Approve selected recipes"
    
    def reject_recipes(self, request, queryset):
        """Reject selected recipes"""
        # Note: You'll need to add rejection reason manually in admin
        updated = queryset.update(
            approval_status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'{updated} recipe(s) rejected.')
    reject_recipes.short_description = "❌ Reject selected recipes"
    
    def mark_as_pending(self, request, queryset):
        """Mark as pending review"""
        updated = queryset.update(approval_status='pending')
        self.message_user(request, f'{updated} recipe(s) marked as pending.')
    mark_as_pending.short_description = "⏳ Mark as pending review"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'recipe__title']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

