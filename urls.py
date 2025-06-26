from django.urls import path
from . import views
from fruits.views import add_fruit, admin_dashboard, all_fruits, edit_fruit, delete_fruit, vendor_dashboard

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/vendor/', vendor_dashboard, name='vendor_dashboard'),
    path('add-fruit/', add_fruit, name='add_fruit'),
    path('fruits/', all_fruits, name='all_fruits'),
    path('fruits/<int:fruit_id>/edit/', edit_fruit, name='edit_fruit'),
    path('fruits/<int:fruit_id>/delete/', delete_fruit, name='delete_fruit'),
]
