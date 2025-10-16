from django.urls import path
from . import api_views

app_name = 'recipes_api'

urlpatterns = [
    # RESTful API endpoints
    path('subscribers/', api_views.SubscriberListCreateView.as_view(), name='subscriber-list-create'),
    path('subscribers/<int:pk>/', api_views.SubscriberDetailView.as_view(), name='subscriber-detail'),

    # Alternative subscription endpoint
    path('subscribe/', api_views.subscribe_via_api, name='subscribe-api'),
]
