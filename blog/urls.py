from django.urls import path
from .views import add_favourite, remove_favourite
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('search/', views.search_results, name='search_results'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('profile/', views.profile_view, name='profile'),
    path('favourites/', views.view_favourites, name='view_favourites'),
    path('comments/', views.view_comments, name='view_comments'),
    path('profile/delete/', views.delete_profile_view, name='delete_profile_view'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('add_favourite/<int:post_id>/', add_favourite, name='add_favourite'),
    path('remove_favourite/<int:post_id>/', remove_favourite, name='remove_favourite'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/edit_comment/<int:comment_id>',
         views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>',
         views.comment_delete, name='comment_delete'),
]