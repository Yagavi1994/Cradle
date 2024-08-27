from .models import Category, Profile

def categories_processor(request):
    """
    To display categories in the navbar.
    """
    categories = Category.objects.all()
    return {'categories': categories}

def user_profile(request):
    """
    To display profile pic in navbar.
    """
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {'profile': profile}
    return {}