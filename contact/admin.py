from django.contrib import admin
from .models import Contact


# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin view for the Contact model.

    **Displays:**

    :field:`name`, :field:`email`, :field:`message`, :field:`created_on`
    """
    list_display = ('name', 'email', 'message', 'created_on')
    search_fields = ('name', 'email')
    list_filter = ('created_on',)
