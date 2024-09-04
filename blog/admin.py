from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment, Category, Favourite, Profile


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin view for the Post model.

    **Displays:**

    :field:`title`, :field:`category`, :field:`slug`, :field:`status`,
    :field:`created_on`

    **Search fields:**

    :field:`title`, :field:`category`, :field:`content`

    **Filters:**

    :field:`status`, :field:`category`

    **Prepopulated Fields:**

    :field:`slug` based on :field:`title`

    **Summernote Fields:**

    :field:`content`
    """
    list_display = ('title', 'category', 'slug', 'status', 'created_on')
    search_fields = ['title', 'category', 'content']
    list_filter = ('status', 'category')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin view for the Comment model.

    This registers the Comment model for management in the admin panel.
    """
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin view for the Category model.

    **Prepopulated Fields:**

    :field:`slug` based on :field:`name`

    **Displays:**

    :field:`name`, :field:`slug`
    """
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    """
    Admin view for the Favourite model.

    **Displays:**

    :field:`author`, :field:`post`
    """
    list_display = ('author', 'post')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin view for the Profile model.

    **Displays:**

    :field:`user`, :field:`profile_picture`, :field:`selected_avatar`,
    :field:`selected_avatar1`, :field:`selected_avatar2`
    """
    list_display = (
        'user', 'profile_picture', 'selected_avatar',
        'selected_avatar1', 'selected_avatar2'
    )
