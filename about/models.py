from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class About(models.Model):
    title = models.CharField(max_length=200, unique=True)
    about_image = CloudinaryField('image', default='profile_pictures/dbtlsekxl5grhsmhvgok')
    updated_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.title
