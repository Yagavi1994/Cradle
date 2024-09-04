from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = (
    (0, "Draft"),
    (1, "Published")
)


class Category(models.Model):
    """
    Model representing post categories.

    **Fields:**

    - name: The name of the category (unique).
    - slug: A unique slug field for the category URL.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Model representing a blog post.

    **Fields:**

    - title: Title of the post.
    - slug: A unique slug for the post URL.
    - author: The author of the post (linked to User).
    - featured_image: The featured image for the post (Cloudinary).
    - source: The source or reference for the post.
    - category: The category the post belongs to (linked to Category).
    - content: The main content of the post.
    - created_on: Timestamp when the post was created.
    - updated_on: Timestamp when the post was last updated.
    - status: The publication status (Draft or Published).
    - excerpt: A short excerpt or summary of the post.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='default_jubihg')
    source = models.CharField(max_length=400)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='posts'
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Model representing comments on blog posts.

    **Fields:**

    - post: The post that the comment is associated with.
    - author: The user who wrote the comment.
    - body: The content of the comment.
    - approved: Whether the comment has been approved.
    - created_on: Timestamp when the comment was created.
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter"
    )
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.body[:20]} by {self.author}"


class Favourite(models.Model):
    """
    Model representing a user's favorite posts.

    **Fields:**

    - author: The user who favorited the post.
    - post: The post that has been favorited.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username} favorited {self.post.title}'


class Profile(models.Model):
    """
    Model representing a user's profile.

    **Fields:**

    - user: The user associated with the profile.
    - profile_picture: A Cloudinary image field for the user's profile picture.
    - selected_avatar: An avatar image selected by the user.
    - selected_avatar1: An alternate avatar option.
    - selected_avatar2: Another alternate avatar option.
    - selected_avatar3: A third alternate avatar option.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField(
        'image', default='nnn7jme2crgxnlba6ygb'
    )
    selected_avatar = CloudinaryField(
        'image', default='avatar1_dw6wb7'
    )
    selected_avatar1 = CloudinaryField(
        'image', default='kjxyk9iaiqwwximms8cc'
    )
    selected_avatar2 = CloudinaryField(
        'image', default='profile_pictures/inuqkebcm65yyrfhsmfj'
    )
    selected_avatar3 = CloudinaryField(
        'image', default='nnn7jme2crgxnlba6ygb'
    )

    def __str__(self):
        return self.user.username

    def get_profile_picture_url(self):
        """
        Returns the URL for the profile picture or selected avatar.
        """
        if self.profile_picture:
            return self.profile_picture.url
        if self.selected_avatar:
            return self.selected_avatar.url
        if self.selected_avatar1:
            return self.selected_avatar1.url
        if self.selected_avatar2:
            return self.selected_avatar2.url
        if self.selected_avatar3:
            return self.selected_avatar3.url
