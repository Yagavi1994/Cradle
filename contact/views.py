from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm
from .models import Contact

# Create your views here.

def contact(request):
    """
    Renders the About page
    """
    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.add_message(request, messages.SUCCESS, "Thank you. Your message is received! I endeavour to respond within 2 working days.")

    contact = Contact.objects.all()
    contact_form = ContactForm()

    return render(
        request,
        'contact/contact.html',
        {"contact": contact,
        "contact_form" : ContactForm},
        )