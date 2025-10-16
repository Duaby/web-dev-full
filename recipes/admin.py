from django.contrib import admin
from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subscribed_at')
    search_fields = ('name', 'email')
    list_filter = ('subscribed_at',)
    ordering = ('-subscribed_at',)
