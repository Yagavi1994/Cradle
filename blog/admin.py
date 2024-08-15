from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment, CATEGORY


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'get_category_display', 'slug', 'status', 'created_on')
    search_fields = ['title', 'category', 'content']
    list_filter = ('status', 'category',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

    def get_search_results(self, request, queryset, search_term):
        """
        Overrides the default search behavior to enable searching by
        category name and genre name.
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Convert the search term to lowercase
        search_term = search_term.lower()

        # Mapping for category names to their corresponding integer values
        category_mapping = {name.lower(): value for value, name in CATEGORY}

        # Check if the search term matches any category name
        if search_term in category_mapping:
            queryset |= self.model.objects.filter(category=category_mapping[search_term])
        return queryset, use_distinct

    def get_category_display(self, obj):
        return dict(CATEGORY).get(obj.category)

    get_category_display.short_description = 'Category'


# Register your models here.

admin.site.register(Comment)