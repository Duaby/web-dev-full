# Generated migration file
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0003_alter_contactmessage_options_alter_recipe_options_and_more'),
    ]

    operations = [
        # Add approval status to Recipe
        migrations.AddField(
            model_name='recipe',
            name='approval_status',
            field=models.CharField(
                choices=[
                    ('draft', 'Draft'),
                    ('pending', 'Pending Review'),
                    ('approved', 'Approved'),
                    ('rejected', 'Rejected')
                ],
                default='approved',
                max_length=20,
                db_index=True
            ),
        ),
        
        # Add flag to distinguish user-submitted recipes
        migrations.AddField(
            model_name='recipe',
            name='is_user_recipe',
            field=models.BooleanField(default=False, db_index=True),
        ),
        
        # Add rejection reason
        migrations.AddField(
            model_name='recipe',
            name='rejection_reason',
            field=models.TextField(blank=True, null=True),
        ),
        
        # Add reviewed by admin
        migrations.AddField(
            model_name='recipe',
            name='reviewed_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='reviewed_recipes',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        
        # Add reviewed date
        migrations.AddField(
            model_name='recipe',
            name='reviewed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        
        # Create Favorite model
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Favorite',
                'verbose_name_plural': 'Favorites',
                'ordering': ['-created_at'],
                'unique_together': {('user', 'recipe')},
            },
        ),
        
        # Add indexes for approval status queries
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['approval_status', '-created_at'], name='recipe_approval_date_idx'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['is_user_recipe', 'approval_status'], name='recipe_user_approval_idx'),
        ),
    ]