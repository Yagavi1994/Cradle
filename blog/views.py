import json
from allauth.account.views import SignupView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cloudinary.uploader import upload
from .models import Post, Comment, Category, Favourite, Profile
from .forms import (
    CommentForm, ProfilePictureForm, DeletePictureForm, CustomSignUpForm
)


# Create your views here.

class PostList(generic.ListView):
    """
    Returns all published posts in :model:`blog.Post` and displays them in
    a page of six posts.

    **Context**

    ``queryset``

    All published instances of :model:`blog.Post`

    ``paginate_by``

    Number of posts per page.

    **Template:**

    :template:`blog/index.html`
    """
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 5


def post_detail(request, slug):
    """
    Displays an individual :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`

    **Models:**

    :model:`blog.Post`, :model:`blog.Comment`, :model:`blog.Favourite`

    **Forms:**

    :form:`blog.CommentForm`
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.user.is_authenticated:
        is_favourite = Favourite.objects.filter(
            post=post, author=request.user
        ).exists()
    else:
        is_favourite = False  # Default for anonymous users

    next_post = Post.objects.filter(
        status=1, created_on__lt=post.created_on
    ).order_by('-created_on').first()
    previous_post = Post.objects.filter(
        status=1, created_on__gt=post.created_on
    ).order_by('created_on').first()

    if request.method == "POST":
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    'Comment submitted and awaiting approval'
                )
                return HttpResponseRedirect(request.path_info)
        else:
            messages.add_message(
                request, messages.ERROR, 'You must be logged in to submit a comment.')  # noqa
            return redirect('account_login')
    else:
        comment_form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
            "is_favourite": is_favourite,
            "next_post": next_post,
            "previous_post": previous_post,
        }
    )


def comment_edit(request, slug, comment_id):
    """
    View to edit an individual comment.

    **Models:**

    :model:`blog.Comment`

    **Forms:**

    :form:`blog.CommentForm`

    **Template:**

    No dedicated template, redirects to `post_detail`
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == "POST":
        if comment.author == request.user:
            comment_form = CommentForm(data=request.POST, instance=comment)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.approved = False
                comment.save()
                messages.add_message(request, messages.SUCCESS, 'Comment updated!')  # noqa
            else:
                messages.add_message(request, messages.ERROR, 'Error updating comment!')  # noqa
        else:
            messages.add_message(request, messages.ERROR, 'You are not authorized to edit this comment!')  # noqa

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    View to delete an individual comment.

    **Models:**

    :model:`blog.Comment`

    **Template:**

    No dedicated template, redirects to `post_detail`
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')  # noqa

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


@login_required
def edit_profile_picture(request):
    """
    Handles the editing or deletion of the user's profile picture.

    **Models:**

    :model:`blog.Profile`

    **Forms:**

    :form:`blog.ProfilePictureForm`

    **Template:**

    :template:`blog/profile.html`
    """
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        if 'delete' in request.POST:
            profile.profile_picture = None
            profile.selected_avatar = None
            profile.selected_avatar1 = None
            profile.selected_avatar2 = None
            profile.selected_avatar3 = None
            profile.save()
            messages.success(request, 'Profile picture deleted successfully')
            return redirect('profile')

        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)  # noqa

        if form.is_valid():
            avatar_choice = form.cleaned_data.get('avatar_choice')
            profile_picture = request.FILES.get('profile_picture')

            if profile_picture:
                profile.profile_picture = profile_picture
                profile.selected_avatar = None
                profile.selected_avatar1 = None
                profile.selected_avatar2 = None
                profile.selected_avatar3 = None
            elif avatar_choice:
                selected_avatar = getattr(profile, avatar_choice)
                profile.profile_picture = selected_avatar
                profile.selected_avatar = None
                profile.selected_avatar1 = None
                profile.selected_avatar2 = None
                profile.selected_avatar3 = None

            profile.save()
            messages.success(request, 'Profile picture changed successfully')
            return redirect('profile')
        else:
            messages.error(request, 'There was an error with your submission.')
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, 'blog/profile.html', {'form': form, 'profile': profile})  # noqa


def category_posts(request, slug):
    """
    Displays posts belonging to a specific category.

    **Models:**

    :model:`blog.Category`, :model:`blog.Post`

    **Template:**

    :template:`blog/category_posts.html`
    """
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    paginate_by = 5

    # Set up pagination
    paginator = Paginator(posts, paginate_by)
    page = request.GET.get('page')

    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': paginated_posts,
    })


@login_required
def profile_view(request):
    """
    Displays the user's profile, including their profile picture, comments,
    and favourites.

    **Models:**

    :model:`blog.Profile`, :model:`blog.Favourite`, :model:`blog.Comment`

    **Forms:**

    :form:`blog.ProfilePictureForm`, :form:`blog.DeletePictureForm`

    **Template:**

    :template:`blog/profile.html`
    """
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        if 'confirm' in request.POST:
            form = ProfilePictureForm(
                request.POST, request.FILES, instance=profile
            )
            if form.is_valid():
                form.save()
                messages.add_message(
                    request, messages.SUCCESS, 'Profile picture changed successfully!')  # noqa
            else:
                messages.add_message(
                    request, messages.ERROR, 'Error updating the picture, try again later!')  # noqa
            return redirect('profile')
        elif 'delete' in request.POST:
            try:
                profile.profile_picture = 'nnn7jme2crgxnlba6ygb'
                profile.save()
                messages.add_message(
                    request, messages.SUCCESS, 'Profile picture deleted successfully!')  # noqa
            except Exception as e:
                messages.add_message(
                    request, messages.ERROR, 'Error deleting the picture, try again later!')  # noqa

            return redirect('profile')

    else:
        form = ProfilePictureForm(instance=profile)
        delete_form = DeletePictureForm()

    favourites = Favourite.objects.filter(author=request.user)
    comments = Comment.objects.filter(author=request.user)

    context = {
        'form': form,
        'delete_form': delete_form,
        'profile': profile,
        'favourites': favourites,
        'comments': comments,
    }

    return render(request, 'blog/profile.html', context)


@login_required
def delete_profile_view(request):
    """
    Displays a view where users can confirm the deletion of their profile.

    **Template:**

    :template:`blog/delete_profile.html`
    """
    if request.method == 'POST':
        return render(request, 'blog/delete_profile.html')
    else:
        return redirect('profile')


@login_required
def view_favourites(request):
    """
    Displays a list of a user's favourite posts.

    **Models:**

    :model:`blog.Favourite`

    **Template:**

    :template:`blog/favourites.html`
    """
    favourites = Favourite.objects.filter(author=request.user).select_related(
        'post'
    )
    paginate_by = 5

    # Set up pagination
    paginator = Paginator(favourites, paginate_by)
    page = request.GET.get('page')

    try:
        paginated_favourites = paginator.page(page)
    except PageNotAnInteger:
        paginated_favourites = paginator.page(1)
    except EmptyPage:
        paginated_favourites = paginator.page(paginator.num_pages)

    return render(request, 'blog/favourites.html', {
        'favourites': paginated_favourites,
        'is_paginated': paginated_favourites.has_other_pages(),
        'page_obj': paginated_favourites,
    })


def add_remove_favourite(request):
    """
    Allows authenticated users to add or remove a post from their favourites
    list.

    **Models:**

    :model:`blog.Favourite`, :model:`blog.Post`

    **Template:**

    No dedicated template, returns a JSON response.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'not_authenticated'}, status=401)  # noqa

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')

            if not post_id:
                return JsonResponse({'success': False, 'error': 'Post ID not provided'}, status=400)  # noqa

            post = get_object_or_404(Post, id=post_id)

            favourite, created = Favourite.objects.get_or_create(
                post=post, author=request.user
            )

            if not created:
                favourite.delete()
                return JsonResponse({'success': True, 'added': False})

            return JsonResponse({'success': True, 'added': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)  # noqa

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)  # noqa


@login_required
def view_comments(request):
    """
    Displays a list of comments created by the user.

    **Models:**

    :model:`blog.Comment`

    **Template:**

    :template:`blog/comments.html`
    """
    comments = Comment.objects.filter(author=request.user).select_related('post')
    comment_count = comments.count()  # Count the number of comments
    paginate_by = 5

    # Set up pagination
    paginator = Paginator(comments, paginate_by)
    page = request.GET.get('page')

    try:
        paginated_comments = paginator.page(page)
    except PageNotAnInteger:
        paginated_comments = paginator.page(1)
    except EmptyPage:
        paginated_comments = paginator.page(paginator.num_pages)

    return render(request, 'blog/comments.html', {
        'comments': paginated_comments,
        'is_paginated': paginated_comments.has_other_pages(),
        'page_obj': paginated_comments,
        'comment_count': comment_count,
    })


@login_required
def delete_profile(request):
    """
    Deletes the user's profile upon confirmation.

    **Template:**

    :template:`account/login.html`
    """
    if request.method == 'POST':
        try:
            request.user.delete()
            messages.add_message(
                request, messages.SUCCESS, 'Profile deleted successfully!'
            )
            return redirect('home')
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Profile does not exist!')  # noqa
            return redirect('profile')
    return render(request, 'account/login.html')


class CustomSignupView(SignupView):
    """
    Custom sign-up view to redirect users to the email verification page
    after successful signup.

    **Forms:**

    :form:`blog.CustomSignUpForm`

    **Template:**

    No dedicated template, uses the default sign-up flow.
    """
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(reverse_lazy('account_email_verification_sent'))


def signup(request):
    """
    Displays the signup form and handles user registration.

    **Forms:**

    :form:`blog.CustomSignUpForm`

    **Template:**

    :template:`signup.html`
    """
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_login')  # noqa
    else:
        form = CustomSignUpForm()

    return render(request, 'signup.html', {'form': form})
