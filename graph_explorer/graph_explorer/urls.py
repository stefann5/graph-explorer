from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('graph_explorer_platform.urls')),
]
