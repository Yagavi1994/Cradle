from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from blog.forms import CustomPasswordResetForm

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm), name='password_reset'),]
