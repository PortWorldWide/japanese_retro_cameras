from django.urls import path
from . import views

urlpatterns = [
    path('search-autocomplete/', views.search_autocomplete, name='search_autocomplete'),
]