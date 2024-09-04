from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm
from .models import Contact


def contact(request):
    """
    Renders the Contact page and handles form submissions.

    **Models:**

    :model:`contact.Contact`

    **Forms:**

    :form:`contact.ContactForm`

    **Template:**

    :template:`contact/contact.html`
    """
    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                "Thank you. Your message is received! I endeavour to respond "
                "within 2 working days."
            )

    contact = Contact.objects.all()
    contact_form = ContactForm()

    return render(
        request,
        'contact/contact.html',
        {
            "contact": contact,
            "contact_form": contact_form,
        },
    )
