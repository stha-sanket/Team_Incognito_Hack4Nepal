from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('chatbot/', views.ChatbotView.as_view(), name='chatbot'),
    path('extractor/', views.ExtractorView.as_view(), name='extractor'),
] 