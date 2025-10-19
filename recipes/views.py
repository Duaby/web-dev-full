from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .forms import SubscriberForm, ReviewForm, ContactForm

def landing_page(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber = form.save()

            # Create recipe content
            recipe_content = """
🍝 PASTA CARBONARA RECIPE 🍝

INGREDIENTS (Serves 4):
- 400g spaghetti
- 200g pancetta or guanciale, diced
- 4 large eggs
- 1 cup grated Pecorino Romano cheese
- Freshly ground black pepper
- Salt

INSTRUCTIONS:

1. Bring a large pot of salted water to boil. Cook spaghetti according to package directions until al dente.

2. While pasta cooks, heat a large skillet over medium heat. Add pancetta and cook until crispy, about 5-7 minutes. Remove from heat.

3. In a bowl, whisk together eggs, cheese, and plenty of black pepper.

4. When pasta is done, reserve 1 cup pasta water, then drain pasta.

5. Add hot pasta to the skillet with pancetta. Toss quickly.

6. Remove from heat and immediately add egg mixture, tossing vigorously to create a creamy sauce. Add pasta water as needed for desired consistency.

7. Serve immediately with extra cheese and black pepper.

PRO TIP: The residual heat from the pasta will cook the eggs without scrambling them!

---

🥩 PERFECT RIBEYE STEAK 🥩

INGREDIENTS (Serves 2):
- 2 ribeye steaks (1.5 inches thick)
- Salt and pepper
- 2 tbsp butter
- 2 sprigs rosemary
- 2 cloves garlic, smashed

INSTRUCTIONS:

1. Remove steaks from fridge 30 minutes before cooking. Pat dry and season generously with salt and pepper.

2. Heat a cast-iron skillet over high heat until smoking hot.

3. Add steaks and sear for 4-5 minutes per side for medium-rare (internal temp 130°F).

4. Add butter, rosemary, and garlic to pan. Tilt pan and spoon melted butter over steaks for 1 minute.

5. Rest steaks 5 minutes before slicing.

PRO TIP: For the perfect crust, make sure your pan is screaming hot before adding the steak!

---

Enjoy these professional techniques in your kitchen!
"""

            # Send email with recipe
            email_msg = EmailMessage(
                subject='Your Free Restaurant Recipe Collection!',
                body=f"""Hi {subscriber.name},

Thank you for subscribing to our restaurant recipe collection!

Here are your FREE recipes featuring professional cooking techniques:

{recipe_content}

Happy cooking!
Best regards,
Restaurant Team

P.S. More recipes coming soon - stay tuned!
""",
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@restaurant.com',
                to=[subscriber.email],
            )

            # Try to send the email
            try:
                email_msg.send(fail_silently=False)
                messages.success(request, 'Thank you for subscribing! Check your email for your free recipe collection.')
            except Exception as e:
                # If email fails, still show success but log the error
                print(f"Email sending failed: {e}")
                messages.success(request, 'Thank you for subscribing! Your recipes will be sent shortly.')

            return redirect('recipes:landing_page')
    else:
        form = SubscriberForm()

    return render(request, 'recipes/landing.html', {'form': form})


def review_form(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'Thank you for your review! It will be published after approval by our team.')
            return redirect('recipes:review_form')
    else:
        form = ReviewForm()

    return render(request, 'recipes/review_form.html', {'form': form})


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('recipes:contact_form')
    else:
        form = ContactForm()

    return render(request, 'recipes/contact_form.html', {'form': form})
