from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))
CATEGORY = ((0, "Newborn"), (1, "Breastfeeding"), (2, "Formula Feeding"), (3, "Sleep"), (4, "Baby Led Weaning"), (5, "Eating Habits"), (6, "Potty Training"), (7, "Toddlers"), (8, "Parenting"), (9, "Personal Stories"), (10, "Teens"))

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    source = models.CharField(max_length=400)
    category = models.IntegerField(choices=CATEGORY, default=0)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f"{self.title}"

