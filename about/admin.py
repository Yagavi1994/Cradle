from django.contrib import admin
from .models import About
from django_summernote.admin import SummernoteModelAdmin


@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    """
    Admin view for the About model.

    **Summernote Fields:**

    :field:`content`
    """
    summernote_fields = ('content',)
