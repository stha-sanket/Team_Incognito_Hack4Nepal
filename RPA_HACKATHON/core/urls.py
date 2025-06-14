from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('citizenship/', views.citizenship, name='citizenship'),
    path('pan/', views.pan, name='pan'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-application-status/<int:application_id>/', views.update_application_status, name='update_application_status'),
] 