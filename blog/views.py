import json
from allauth.account.views import SignupView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from cloudinary.uploader import upload
from .models import Post, Comment, Category, Favourite, Profile
from .forms import CommentForm, ProfilePictureForm, DeletePictureForm, CustomSignUpForm


# Create your views here.

class PostList(generic.ListView):
    """
    Returns all published posts in :model:`blog.Post`
    and displays them in a page of six posts. 
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
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()
    
    # Handle favorite status for authenticated users
    if request.user.is_authenticated:
        is_favourite = Favourite.objects.filter(post=post, author=request.user).exists()
    else:
        is_favourite = False  # Default for anonymous users

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
            messages.add_message(request, messages.ERROR, 'You must be logged in to submit a comment.')
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
        }
    )


def comment_edit(request, slug, comment_id):
    """
    View to edit comments
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
                messages.add_message(request, messages.SUCCESS, 'Comment updated!')
            else:
                messages.add_message(request, messages.ERROR, 'Error updating comment!')
        else:
            messages.add_message(request, messages.ERROR, 'You are not authorized to edit this comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    View to delete a comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))



def search_results(request):
    """
    To search in the search bar
    """
    query = request.GET.get('q', '').strip()

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__icontains=query)
        )
    else:
        results = Post.objects.none()
    
    paginate_by = 5

 
    return render(
        request, 
        'blog/search_results.html', 
        {'results': results, 
        'query': query,})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    paginate_by = 5

    
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts,
    })


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        if 'confirm' in request.POST:
            form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Profile picture changed successfully!')
            else:
                messages.add_message(request, messages.ERROR, 'Error updating the picture, try again later!')
            return redirect('profile')
        elif 'delete' in request.POST:
            try:
                profile.profile_picture = 'nnn7jme2crgxnlba6ygb'
                profile.save()
                messages.add_message(request, messages.SUCCESS, 'Profile picture deleted successfully!')
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'Error deleting the picture, try again later!')
    
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
def edit_profile_picture(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle deletion of profile picture
            profile.profile_picture = None
            profile.selected_avatar = None  # Clear the avatar selection
            profile.selected_avatar1 = None
            profile.selected_avatar2 = None
            profile.selected_avatar3 = None
            profile.save()
            messages.success(request, 'Profile picture deleted successfully')
            return redirect('profile')

        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            avatar_choice = form.cleaned_data.get('avatar_choice')
            profile_picture = request.FILES.get('profile_picture')  # Get directly from FILES

            if profile_picture:
                profile.profile_picture = profile_picture
                # Clear any previously selected avatar since a custom picture is uploaded
                profile.selected_avatar = None
                profile.selected_avatar1 = None
                profile.selected_avatar2 = None
                profile.selected_avatar3 = None
            elif avatar_choice:
                # If no custom picture is uploaded, process the avatar selection
                selected_avatar = getattr(profile, avatar_choice)
                profile.profile_picture = selected_avatar
                # Clear other avatars
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

    return render(request, 'blog/profile.html', {'form': form, 'profile': profile})


@login_required
def delete_profile_view(request):
    if request.method == 'POST':
        return render(request, 'blog/delete_profile.html')
    else:
        return redirect('profile')


@login_required
def view_favourites(request):
    favourites = Favourite.objects.filter(author=request.user).select_related('post')
    return render(request, 'blog/favourites.html', {'favourites': favourites})
    

@login_required
def add_remove_favourite(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')

            if not post_id:
                return JsonResponse({'success': False, 'error': 'Post ID not provided'})

            post = get_object_or_404(Post, id=post_id)

            favourite, created = Favourite.objects.get_or_create(post=post, author=request.user)

            if not created:
                favourite.delete()
                return JsonResponse({'success': True, 'added': False})

            return JsonResponse({'success': True, 'added': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})

    return JsonResponse({'success': False})
    

@login_required
def view_comments(request):
    comments = Comment.objects.filter(author=request.user).select_related('post')
  
    return render(request, 'blog/comments.html', {'comments': comments})



@login_required
def delete_profile(request):
    if request.method == 'POST':
        try:
            request.user.delete()
            messages.add_message(request, messages.SUCCESS, 'Profile deleted Successfully!')
            return redirect('home')
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Profile does not exist!')
            return redirect('profile')
    return render(request, 'account/login.html')



class CustomSignupView(SignupView):

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(reverse_lazy('account_email_verification_sent'))


def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_login')  # or wherever you want to redirect after signup
    else:
        form = CustomSignUpForm()
    
    return render(request, 'signup.html', {'form': form})
