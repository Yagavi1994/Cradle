from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Comment, Category, Favourite, Profile
from .forms import CommentForm, ProfilePictureForm, DeletePictureForm


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
    if request.method == "POST":
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

    comment_form = CommentForm()

    return render(
        request, 
        "blog/post_detail.html", 
        {"post": post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form" : CommentForm,},
        )

def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))

def comment_delete(request, slug, comment_id):
    """
    view to delete comment
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
            Q(category__name__icontains=query)
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
                return redirect('profile')
        elif 'delete' in request.POST:
            profile.profile_picture = 'nnn7jme2crgxnlba6ygb'
            profile.save()
            messages.add_message(request, messages.SUCCESS, 'Profile picture deleted successfully!')
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
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, 'blog/preview_profile_picture.html', {'profile': profile})
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, 'blog/edit_profile_picture.html', {'form': form, 'profile': profile})

@login_required
def confirm_profile_picture(request):
    return redirect('profile')


@login_required
def delete_profile_view(request):
    if request.method == 'POST':
        return render(request, 'blog/delete_profile.html')
    else:
        return redirect('profile')

@require_POST
@login_required
def add_favourite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Favourite.objects.get_or_create(author=request.user, post=post)
    return JsonResponse({'status': 'added'})

@require_POST
@login_required
def remove_favourite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    favourite = Favourite.objects.filter(author=request.user, post=post)
    if favourite.exists():
        favourite.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'not found'})

@login_required
def view_favourites(request):
    favourites = Favourite.objects.filter(author=request.user)
    return render(request, 'blog/favourites.html', {'favourites': favourites})

@login_required
def view_comments(request):
    comments = Comment.objects.filter(author=request.user)
    return render(request, 'blog/comments.html', {'comments': comments})

@login_required
def delete_profile(request):
    if request.method == 'POST':
            request.user.delete()
            messages.add_message(request, messages.SUCCESS, 'Profile deleted Successfully!')
    return render(request, 'account/login.html')