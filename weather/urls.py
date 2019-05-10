from django.urls import path
from . import views


urlpatterns = [
    path('delete/<name>/', views.delete),
    path('', views.index),
]
