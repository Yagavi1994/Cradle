from .models import Category

def categories_processor(request):
    """
    To display categories in the navbar
    """
    categories = Category.objects.all()
    return {'categories': categories}