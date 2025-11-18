"""URLs for users app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('create/', views.create_user, name='create_user'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('<int:user_id>/edit/', views.edit_user_profile, name='edit_user_profile'),
    path('<int:user_id>/change-password/', views.change_user_password, name='change_user_password'),
    path('<int:user_id>/toggle-admin/', views.toggle_admin, name='toggle_admin'),
    path('<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
