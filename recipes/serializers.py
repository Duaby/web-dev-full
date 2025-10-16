from rest_framework import serializers
from .models import Subscriber

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'name', 'email', 'subscribed_at']
        read_only_fields = ['id', 'subscribed_at']

    def create(self, validated_data):
        # Check for duplicate email
        email = validated_data.get('email')
        if Subscriber.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already subscribed."})
        return super().create(validated_data)
