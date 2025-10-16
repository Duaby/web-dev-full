from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Subscriber
from .serializers import SubscriberSerializer

class SubscriberListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing all subscribers and creating new ones.
    GET: List all subscribers
    POST: Create a new subscriber and send welcome email
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    def perform_create(self, serializer):
        subscriber = serializer.save()
        # Send welcome email
        self.send_welcome_email(subscriber)

    def send_welcome_email(self, subscriber):
        subject = 'Welcome to Our Restaurant Recipe Collection!'
        message = f"""
        Hi {subscriber.name},

        Thank you for subscribing to our restaurant recipe collection!

        Here are two exclusive recipes just for you:

        🍝 PASTA CARBONARA
        Ingredients:
        - 200g spaghetti
        - 100g pancetta or bacon
        - 2 large eggs
        - 50g grated Pecorino Romano cheese
        - Black pepper
        - Salt

        Instructions:
        1. Cook pasta in salted boiling water
        2. Cook pancetta until crispy
        3. Mix eggs and cheese in a bowl
        4. Combine hot pasta with pancetta
        5. Add egg mixture off heat, stirring quickly
        6. Season with black pepper

        🥩 RIBEYE STEAK
        Ingredients:
        - 1 ribeye steak (1.5 inches thick)
        - Salt and pepper
        - 2 tbsp butter
        - Fresh herbs (rosemary/thyme)

        Instructions:
        1. Season steak generously with salt and pepper
        2. Heat cast iron skillet until very hot
        3. Sear steak 4-5 minutes per side for medium-rare
        4. Add butter and herbs in last minute
        5. Rest steak 5 minutes before slicing

        Pro Tip: Always let steak come to room temperature before cooking!

        Happy cooking!
        Restaurant Recipe Team
        """

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email],
            )
            email.send()
        except Exception as e:
            # Log error but don't fail the API call
            print(f"Email sending failed: {e}")

class SubscriberDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting individual subscribers.
    GET: Retrieve subscriber details
    PUT/PATCH: Update subscriber
    DELETE: Remove subscriber
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

@api_view(['POST'])
def subscribe_via_api(request):
    """
    Alternative API endpoint for subscription that matches the web form behavior.
    """
    serializer = SubscriberSerializer(data=request.data)
    if serializer.is_valid():
        subscriber = serializer.save()
        # Send welcome email
        subject = 'Welcome to Our Restaurant Recipe Collection!'
        message = f"""
        Hi {subscriber.name},

        Thank you for subscribing to our restaurant recipe collection!

        Here are two exclusive recipes just for you:

        🍝 PASTA CARBONARA
        Ingredients:
        - 200g spaghetti
        - 100g pancetta or bacon
        - 2 large eggs
        - 50g grated Pecorino Romano cheese
        - Black pepper
        - Salt

        Instructions:
        1. Cook pasta in salted boiling water
        2. Cook pancetta until crispy
        3. Mix eggs and cheese in a bowl
        4. Combine hot pasta with pancetta
        5. Add egg mixture off heat, stirring quickly
        6. Season with black pepper

        🥩 RIBEYE STEAK
        Ingredients:
        - 1 ribeye steak (1.5 inches thick)
        - Salt and pepper
        - 2 tbsp butter
        - Fresh herbs (rosemary/thyme)

        Instructions:
        1. Season steak generously with salt and pepper
        2. Heat cast iron skillet until very hot
        3. Sear steak 4-5 minutes per side for medium-rare
        4. Add butter and herbs in last minute
        5. Rest steak 5 minutes before slicing

        Pro Tip: Always let steak come to room temperature before cooking!

        Happy cooking!
        Restaurant Recipe Team
        """

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email],
            )
            email.send()
        except Exception as e:
            print(f"Email sending failed: {e}")

        return Response({
            'message': 'Successfully subscribed! Check your email for recipes.',
            'subscriber': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
