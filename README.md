I built this restaurant website with recipe management. to manage recipes, categories, reviews, subscribers, and contact messages. The site includes a web interface and REST API.

How it works:
1. Users visit the landing page to browse recipes.
2. I add and manage recipes through the Django admin panel.
3. New subscribers receive welcome emails with a sample recipe.
4. Users submit reviews that require admin approval before display.
5. Contact messages arrive through forms and appear in admin.
6. API endpoints provide data access for external integrations.

Built with:
- Django 5.2.7 for web framework
- Django REST Framework for API
- Django-filter for search and filtering
- Django-cors-headers for cross-origin requests
- Gmail SMTP for email delivery

To run locally:
1. Install Python 3.8 or higher.
2. Clone the repository.
3. Install dependencies: pip install -r requirements.txt
4. Run migrations: python manage.py makemigrations
5. Apply migrations: python manage.py migrate
6. Create superuser: python manage.py createsuperuser
7. Start server: python manage.py runserver
8. Open http://127.0.0.1:8000/
9. Access admin at http://127.0.0.1:8000/admin/
10. Use API at http://127.0.0.1:8000/api/

To run with Docker:
1. Install Docker and Docker Compose.
2. Run: docker-compose up --build
3. Open http://localhost:8000/
4. Access admin at http://localhost:8000/admin/
5. Use API at http://localhost:8000/api/
