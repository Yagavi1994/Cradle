from django.urls import path
from .views import add_remove_favourite, profile_view, edit_profile_picture, edit_profile_picture, confirm_profile_picture
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
    path('add_remove_favourite/', views.add_remove_favourite, name='add_remove_favourite'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/edit_comment/<int:comment_id>',
         views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>',
         views.comment_delete, name='comment_delete'),
]