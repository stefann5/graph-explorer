from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('select-plugin/', views.select_plugin, name="select_plugin"),
    path('select-file/', views.select_file, name="select_file"),
    path('search/', views.search, name="search_graph"),
    path('filter/', views.filter, name="filter_graph"),
    path('get-installed-plugins/', views.get_available_plugins, name="get_installed_plugins"),
    path('toggle-view/', views.toggle_view, name="toggle_view"),
    path('api/add_node/', views.add_node, name='add_node'),
    path('api/update_node/', views.update_node, name='update_node'),
    path('api/delete_node/', views.delete_node, name='delete_node'),
    path('api/add_edge/', views.add_edge, name='add_edge'),
    path('api/update_edge/', views.update_edge, name='update_edge'),
    path('api/delete_edge/', views.delete_edge, name='delete_edge'),
    path('api/delete_graph/', views.delete_graph, name='delete_graph'),
    path('api/search_graph/', views.search_graph, name='search_graph'),
    path('api/filter_graph/', views.filter_graph, name='filter_graph')
]
