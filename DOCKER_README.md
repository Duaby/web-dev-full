# Docker Setup for Django Restaurant Recipe Landing Page

This guide explains how to run the Django Restaurant Recipe Landing Page application using Docker and Docker Compose.

## 📋 Prerequisites

- Docker installed on your system
- Docker Compose installed on your system
- Gmail account with app password (for email functionality)

## 🚀 Quick Start

### Step 1: Clone/Download the Project
```bash
cd /path/to/your/project
```

### Step 2: Configure Email (Optional but Recommended)
Edit `docker-compose.yml` and replace the email credentials:
```yaml
environment:
  - DJANGO_SETTINGS_MODULE=restaurant_web.settings
  - EMAIL_HOST_USER=your-actual-gmail@gmail.com
  - EMAIL_HOST_PASSWORD=your-16-character-app-password
```

**To get Gmail app password:**
1. Go to Google Account → Security → 2-Step Verification → App passwords
2. Generate a 16-character password
3. Use it in the environment variables above

### Step 3: Build the Docker Image
```bash
docker-compose build
```
This creates a Docker image with Python 3.11 and installs all required dependencies.

### Step 4: Run Database Migrations (First Time Only)
```bash
docker-compose run --rm web python manage.py migrate
```
This sets up the SQLite database with the required tables.

### Step 5: Create Admin User (First Time Only)
```bash
docker-compose run --rm web python manage.py createsuperuser
```
Follow the prompts to create an admin username, email, and password.

### Step 6: Start the Application
```bash
docker-compose up
```
The application will start and be available at http://localhost:8000

## 🌐 Access the Application

Once running, access these URLs:

- **Landing Page**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **API Endpoints**: http://localhost:8000/api/

## 🛠️ Docker Commands Reference

### Start the Application
```bash
docker-compose up
```

### Start in Background (Detached Mode)
```bash
docker-compose up -d
```

### Stop the Application
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs
```

### Rebuild After Code Changes
```bash
docker-compose build --no-cache
docker-compose up
```

### Run Django Management Commands
```bash
# Run migrations
docker-compose run --rm web python manage.py migrate

# Create superuser
docker-compose run --rm web python manage.py createsuperuser

# Run shell
docker-compose run --rm web python manage.py shell

# Run tests
docker-compose run --rm web python manage.py test
```

## 📁 File Structure

```
your-project/
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
├── restaurant_web/        # Django project settings
├── recipes/               # Django app
└── db.sqlite3            # SQLite database (created after migrations)
```

## 🔧 Configuration

### Environment Variables
You can customize the following in `docker-compose.yml`:

- `EMAIL_HOST_USER`: Your Gmail address
- `EMAIL_HOST_PASSWORD`: Your Gmail app password
- Port mapping (default: 8000)

### Database
- Uses SQLite by default (file: `db.sqlite3`)
- Persistent storage via Docker volume
- Data survives container restarts

### Development vs Production
This setup is configured for development. For production:
- Use PostgreSQL instead of SQLite
- Set `DEBUG=False` in settings
- Configure proper static file serving
- Use environment variables for all sensitive data

## 🐛 Troubleshooting

### Port Already in Use
If port 8000 is busy:
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Access at http://localhost:8001
```

### Permission Issues
If you get permission errors:
```bash
sudo chown -R $USER:$USER .
```

### Database Issues
If database gets corrupted:
```bash
rm db.sqlite3
docker-compose run --rm web python manage.py migrate
```

### Email Not Working
- Verify Gmail app password is correct
- Check spam folder
- Ensure 2FA is enabled on Gmail account

## 🔄 Updates

To update the application:
```bash
git pull  # If using git
docker-compose build --no-cache
docker-compose up
```

## 🛑 Stopping and Cleanup

### Stop Application
```bash
docker-compose down
```

### Remove Everything (Including Database)
```bash
docker-compose down -v --rmi all
```

## 📞 Support

If you encounter issues:
1. Check the logs: `docker-compose logs`
2. Verify Docker and Docker Compose are installed
3. Ensure ports are available
4. Check file permissions

---

**Happy Dockerizing! 🐳**
