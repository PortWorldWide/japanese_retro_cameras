from django.urls import path
from . import views

urlpatterns = [
    path('camera/<slug:slug>/', views.camera_detail, name='camera_detail'),
    path('list/', views.camera_list, name='camera_list'),
    path('search/', views.search_results, name='search_results'),
]