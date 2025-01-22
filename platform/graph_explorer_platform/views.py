
import json
import logging
from pathlib import Path
from django.shortcuts import render
from django.apps.registry import apps
from data_source_plugin_xml.sok.graph.explorer.data_source.data_source_plugin_xml import DataSourcePluginXml
from graph_explorer_platform.search import GraphSearchFilter
from sok.graph.explorer.api.services.graph import(
    DataLoaderBase,
    DataVisualizerBase
)
from sok.graph.explorer.api.model.graph import Graph,Node,Edge
from datetime import datetime
from django.http import JsonResponse

def index(request):
    test_data_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
    plugin = apps.get_app_config('graph_explorer_platform').selected_plugin
    params = {
        'file_path': str(test_data_path),
        'directed': True
    }
    apps.get_app_config('graph_explorer_platform').graph=plugin.load_graph(params)
    simple_visualizer=apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
    graph_data={"code":''}
    graph_data["code"]=simple_visualizer.visualize_graph(apps.get_app_config('graph_explorer_platform').graph)
    return render(request, 'main.html', graph_data)

def select_plugin(request):
    if request.method == 'POST':
        query = request.POST.get('query', 1)
        apps.get_app_config('graph_explorer_platform').set_data_source_plugin(query)
        print(apps.get_app_config('graph_explorer_platform').selected_plugin)

    return index(request)


def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('query', '')
        
        filter_service = GraphSearchFilter()
        apps.get_app_config('graph_explorer_platform').graph = filter_service.search(apps.get_app_config('graph_explorer_platform').graph, search_query)
        simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
        graph_data = {"code": simple_visualizer.visualize_graph(apps.get_app_config('graph_explorer_platform').graph)}

        return JsonResponse(graph_data)

def filter(request):
    if request.method == 'POST':
        filter_query = request.POST.get('query', '')
        
        filter_service = GraphSearchFilter()
        apps.get_app_config('graph_explorer_platform').graph = filter_service.filter(apps.get_app_config('graph_explorer_platform').graph, filter_query)
        
        simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
        graph_data = {"code": simple_visualizer.visualize_graph(apps.get_app_config('graph_explorer_platform').graph)}

        return JsonResponse(graph_data)