
import json
import logging
from pathlib import Path
from django.shortcuts import render
from django.apps.registry import apps
from graph_explorer_platform.search import GraphSearchFilter
from sok.graph.explorer.api.services.graph import(
    DataLoaderBase,
    DataVisualizerBase
)
from sok.graph.explorer.api.model.graph import Graph,Node,Edge
from datetime import datetime
from django.http import JsonResponse

def index(request):
    test_data_path = Path("test_data.json")
    plugin = apps.get_app_config('graph_explorer_platform').data_source_plugins[0]
    params = {
        'file_path': str(test_data_path),
        'directed': True
    }
    apps.get_app_config('graph_explorer_platform').graph=plugin.load_graph(params)
    simple_visualizer=apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
    graph_data={"code":''}
    graph_data["code"]=simple_visualizer.visualize_graph(apps.get_app_config('graph_explorer_platform').graph)
    return render(request, 'main.html', graph_data)

def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('query', '')
        plugin = apps.get_app_config('graph_explorer_platform').data_source_plugins[0]
        params = {
            'file_path': str(Path("test_data.json")),
            'directed': True
        }
        
        filter_service = GraphSearchFilter()
        apps.get_app_config('graph_explorer_platform').graph = filter_service.search(apps.get_app_config('graph_explorer_platform').graph, search_query)
        simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
        graph_data = {"code": simple_visualizer.visualize_graph(apps.get_app_config('graph_explorer_platform').graph)}
        return JsonResponse(graph_data)

def filter(request):
    if request.method == 'POST':
        filter_query = request.POST.get('query', '')
        plugin = apps.get_app_config('graph_explorer_platform').data_source_plugins[0]
        params = {
            'file_path': str(Path("test_data.json")),
            'directed': True
        }
        
        filter_service = GraphSearchFilter()
        apps.get_app_config('graph_explorer_platform').graph = filter_service.filter(apps.get_app_config('graph_explorer_platform').graph, filter_query)
        
        simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
        graph_data = {"code": simple_visualizer.visualize_graph(apps.get_app_config('graph_explorer_platform').graph)}
        return JsonResponse(graph_data)