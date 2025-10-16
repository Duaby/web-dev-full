# Django Restaurant Recipe Landing Page

A complete Django web application for collecting email subscribers and sending them professional restaurant recipes via email. Features a responsive landing page, admin panel, REST API, and automated email delivery.

## 🚀 Features

- **Landing Page**: Responsive subscription form with professional design
- **Email Delivery**: Automatic recipe emails with professional cooking techniques
- **Database Storage**: SQLite database with subscriber management
- **Admin Panel**: Full Django admin interface for managing subscribers
- **REST API**: Complete CRUD operations for subscribers
- **Form Validation**: Duplicate email prevention and input validation
- **Security**: CSRF protection and secure email configuration
- **Responsive Design**: Mobile-friendly layout

## 📋 Prerequisites

- Python 3.8+
- Django 5.2+
- Django REST Framework
- Gmail account (for email sending)

## 🛠️ Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/your/project
   ```

2. **Install dependencies**
   ```bash
   pip install django djangorestframework
   ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser for admin access**
   ```bash
   python manage.py createsuperuser
   ```

## 📧 Email Configuration

### For Production (Real Email Sending)

1. **Generate Gmail App Password:**
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Generate a 16-character app password

2. **Update settings.py:**
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-gmail@gmail.com'  # Your Gmail address
   EMAIL_HOST_PASSWORD = 'your-16-char-app-password'  # App password
   DEFAULT_FROM_EMAIL = 'your-gmail@gmail.com'  # Your Gmail address
   ```

### For Development (Console Output)

Keep the default console backend to see emails in terminal:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 🚀 Running the Application

1. **Start the development server**
   ```bash
   python manage.py runserver
   ```

2. **Access the application:**
   - Landing Page: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Endpoints: http://127.0.0.1:8000/api/

## 📱 Usage

### Web Interface

1. **Subscribe via Landing Page:**
   - Visit http://127.0.0.1:8000/
   - Fill out the subscription form
   - Receive immediate confirmation and recipe email

2. **Admin Panel:**
   - Login at http://127.0.0.1:8000/admin/
   - View/manage subscribers
   - Export subscriber data

### REST API

The application provides a complete REST API for subscriber management:

#### Endpoints

- `GET /api/subscribers/` - List all subscribers
- `POST /api/subscribers/` - Create new subscriber (sends email)
- `GET /api/subscribers/{id}/` - Get specific subscriber
- `PUT /api/subscribers/{id}/` - Update subscriber
- `DELETE /api/subscribers/{id}/` - Delete subscriber

#### API Examples

**Create Subscriber (with email sending):**
```bash
curl -X POST http://127.0.0.1:8000/api/subscribers/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

**List Subscribers:**
```bash
curl http://127.0.0.1:8000/api/subscribers/
```

**Get Specific Subscriber:**
```bash
curl http://127.0.0.1:8000/api/subscribers/1/
```

**Update Subscriber:**
```bash
curl -X PUT http://127.0.0.1:8000/api/subscribers/1/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "email": "jane@example.com"}'
```

**Delete Subscriber:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/subscribers/1/
```

#### API Response Format

**Success Response (201 Created):**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "subscribed_at": "2025-10-15T13:57:35.123456Z"
}
```

**Error Response (400 Bad Request):**
```json
{
    "email": ["This email is already subscribed."]
}
```

## 📊 Database Schema

### Subscriber Model

```python
class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
```

## 🎨 Templates

### Landing Page (`recipes/templates/recipes/landing.html`)

Features:
- Responsive Bootstrap design
- CSRF-protected subscription form
- Success/error message display
- Professional restaurant styling

## 🔧 Project Structure

```
restaurant_web/
├── restaurant_web/          # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py
├── recipes/                # App directory
│   ├── models.py          # Database models
│   ├── views.py           # Web views
│   ├── api_views.py       # REST API views
│   ├── serializers.py     # API serializers
│   ├── forms.py           # Django forms
│   ├── urls.py            # App URL patterns
│   ├── api_urls.py        # API URL patterns
│   ├── admin.py           # Admin configuration
│   └── templates/recipes/
│       └── landing.html   # Landing page template
├── manage.py              # Django management script
└── db.sqlite3            # SQLite database
```

## 🔒 Security Features

- CSRF protection on all forms
- Email uniqueness validation
- Secure password handling for Gmail app passwords
- Django's built-in security middleware
- Input validation and sanitization

## 📧 Email Content

Subscribers receive professional recipes including:

- **Pasta Carbonara**: Traditional Italian technique
- **Perfect Ribeye Steak**: Restaurant-quality cooking method

Emails include detailed instructions, ingredients, and pro tips.

## 🚀 Deployment

For production deployment:

1. Set `DEBUG = False`
2. Configure production database (PostgreSQL recommended)
3. Set up proper email service (SendGrid, Mailgun, etc.)
4. Configure static files serving
5. Set up HTTPS
6. Use environment variables for sensitive data

## 🐛 Troubleshooting

### Common Issues

**Emails not sending:**
- Check Gmail app password is correct
- Verify 2FA is enabled on Gmail account
- Check spam folder

**Form validation errors:**
- Ensure email format is valid
- Check for duplicate email addresses

**Template not found:**
- Verify template paths in settings.py
- Check file permissions

**Database errors:**
- Run `python manage.py migrate`
- Check database file permissions

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review Django documentation
- Open an issue on GitHub

---

**Happy cooking! 🍳**
