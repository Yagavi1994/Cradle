from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment, Category

# Register your models here.

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'category', 'slug', 'status', 'created_on')
    search_fields = ['title', 'category', 'content']
    list_filter = ('status', 'category',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

admin.site.register(Comment)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')