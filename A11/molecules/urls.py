"""URL configuration for molecules app."""
from django.urls import path
from . import views

app_name = 'molecules'

urlpatterns = [
    path('', views.home, name='home'),
    path('chembl/', views.chembl, name='chembl'),
    path('povray/', views.povray, name='povray'),
]
