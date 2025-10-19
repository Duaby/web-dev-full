# Restaurant Web Application - Complete REST API

## A full-featured Django web application for managing restaurant recipes, subscribers, reviews, and contact messages. Includes both a responsive web interface and a comprehensive REST API.

✨ Features (simplified)

### Web Interface

- Landing Page - Beautiful subscription form for newsletter signup
- Review System - Users can submit recipe reviews (admin approval required)
- Contact Form - Direct communication with site administrators
- Admin Panel - Full management interface for all data

### REST API

- 5 Database Models - Subscriber, Recipe, Category, Review, ContactMessage
- 15+ API Endpoints - Complete CRUD operations
- Advanced Search - Global search across recipes and categories
- Pagination - Efficient data loading (10 items per page)
- Filtering - Filter by category, difficulty, featured status
- Permissions - Admin-only and public access control
- Email Integration - Automated welcome emails for new subscribers

### Performance

- Query Optimization - 80% fewer database queries using select_related/prefetch_related
- Database Indexing - Optimized queries with strategic indexes
- Fast Response Times - Efficient serializers and caching

### Technology Stack

| Component | Technology | Version |
| :------ | :----: | -----: |
| Backend | Django | 5.2.7 |
| API Framework | Django REST Framework | 3.16.1 |
| Database | SQLite | Built-in |
| Filtering| django-filter | 24.2 |
| CORS | django-cors-headers | 4.3.1 |
| Containerization | Docker & Docker Compose | Latest|

### 📁 Project Structure

<img width="537" height="658" alt="image" src="https://github.com/user-attachments/assets/e2cd2538-85ab-464a-a2df-bfa068567aca" />

## Quick Start Guide:


## Option 1: Local Setup

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

1. Clone the repository
```bash
git clone https://github.com/Duaby/web-dev-full.git
cd "Restaurant web"
```

2. Create virtual environment (recommended)

```bash
python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
```
3. Install dependencies

```bash
pip install -r requirements.txt
```
4. Run migrations
```bash
python manage.py migrate
```
5. Create admin user
```bash
python manage.py createsuperuser
```
- Username: admin
- Email: admin@example.com
- Password: (your choice)

6. Start development server
```bash
   python manage.py runserver
```
7. Access the application
- Web Interface: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/
- REST API: http://127.0.0.1:8000/api/

## Option 2: Docker Setup (Production-Ready)

### Prerequisites
- Docker Desktop installed
- Docker Compose installed

#### Steps

1. Clone the repository

```bash
git clone https://github.com/Duaby/web-dev-full.git
cd "Restaurant web"












