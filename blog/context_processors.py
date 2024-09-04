from .models import Category, Profile


def categories_processor(request):
    """
    Context processor to provide all categories for display in the navbar.

    **Returns:**

    A dictionary containing the list of categories.
    """
    categories = Category.objects.all()
    return {'categories': categories}


def user_profile(request):
    """
    Context processor to provide the user's profile picture for display in
    the navbar.

    **Returns:**

    A dictionary containing the user's profile if authenticated, otherwise
    an empty dictionary.
    """
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {'profile': profile}
    return {}
