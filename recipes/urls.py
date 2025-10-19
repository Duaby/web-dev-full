from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('review/', views.review_form, name='review_form'),
    path('contact/', views.contact_form, name='contact_form'),
]
