This project builds a restaurant website with recipe management. You manage recipes, categories, reviews, subscribers, and contact messages. The site includes a web interface and REST API.

The application works as follows. Users view recipes on the landing page. You add recipes through the admin panel. The system sends welcome emails to new subscribers. Reviews require approval before display. Contact messages arrive via forms.

You build this with Django 5.2.7. The framework handles models, views, and templates. Django REST Framework provides API endpoints. Django-filter enables search and filtering. Django-cors-headers supports cross-origin requests. Email uses Gmail SMTP.

To run the project, install Python 3.8 or higher. Clone the repository. Install dependencies with pip install -r requirements.txt. Run python manage.py makemigrations. Run python manage.py migrate. Create a superuser with python manage.py createsuperuser. Start the server with python manage.py runserver. Open http://127.0.0.1:8000/ in your browser. Access the admin at http://127.0.0.1:8000/admin/. Use the API at http://127.0.0.1:8000/api/.
