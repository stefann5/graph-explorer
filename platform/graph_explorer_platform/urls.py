from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('select-plugin/', views.select_plugin, name="select_plugin"),
    path('search/', views.search, name="search_graph"),
    path('filter/', views.filter, name="filter_graph"),
]
