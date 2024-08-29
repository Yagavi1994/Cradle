from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"))


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='default_jubihg')
    source = models.CharField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)
    tags = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"

class Favourite(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username} favourite {self.post.title}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField('image', default='nnn7jme2crgxnlba6ygb')
    selected_avatar = CloudinaryField('image', default='profile_pictures/mlu4iynnxdgpam21jrli')
    selected_avatar1 = CloudinaryField('image', default='profile_pictures/cd4uhjgqvhj0kbwcmtqk')
    selected_avatar2 = CloudinaryField('image', default='profile_pictures/y7wgg6bw81hry1cs5bap')

    def __str__(self):
        return self.user.username

    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url 
        if self.selected_avatar:
            return self.selected_avatar.url
        if self.selected_avatar1:
            return self.selected_avatar1.url
        if self.selected_avatar2:
            return self.selected_avatar2.url  
        
