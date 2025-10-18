# DjangoFrameworkWebsiteProject


## 1. Copy my code into these files:
   
- Click on each artifact (code box) I created and copy the content:

📄 recipes/models.py - Copy from the "models.py" artifact

📄 recipes/forms.py - Create new file, copy from "forms.py" artifact

📄 recipes/views.py - Replace content with "views.py" artifact

📄 recipes/urls.py - Create new file, copy from "urls.py" artifact

📄 recipes/admin.py - Replace content with "admin.py" artifact

## 2. Create the templates folder:
- copy paste -> mkdir -p recipes/templates/recipes
Then create recipes/templates/recipes/landing.html and copy the HTML from the first artifact.

## 3. Edit your main settings.py:
- Open restaurant_project/settings.py and add:
```python

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recipes',  # ← ADD THIS LINE
]

# At the bottom, add email settings (for testing):
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 4.  Edit your main urls.py:
### Open restaurant_project/urls.py:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),  # ← ADD THIS LINE
]

```
## 5.Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```
## 6. Create admin user:
```bash 
python manage.py createsuperuser
```
(Enter username, email, and password)

## 7. Run the server:
```bash
python manage.py runserver
```

## 8.Open your browser:
- Go to: http://127.0.0.1:8000/

  
