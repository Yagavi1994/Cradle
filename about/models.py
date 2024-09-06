from django.db import models
from cloudinary.models import CloudinaryField


class About(models.Model):
    """
    Model representing the About section of a website.

    **Fields:**

    - title: The title of the About section (unique).
    - about_image: The Cloudinary image for the About section.
    - updated_on: The timestamp when the About section was last updated.
    - content: The text content for the About section.
    """
    title = models.CharField(max_length=200, unique=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.title
