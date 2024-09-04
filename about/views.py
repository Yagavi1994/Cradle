from django.shortcuts import render
from .models import About


def about_me(request):
    """
    Renders the About page with the latest information from the About model.

    **Models:**

    :model:`about.About`

    **Template:**

    :template:`about/about.html`
    """
    about = About.objects.all().order_by('-updated_on').first()

    return render(
        request,
        "about/about.html",
        {"about": about},
    )
