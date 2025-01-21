
import json
import logging
from pathlib import Path
from django.shortcuts import render
from django.apps.registry import apps
from sok.graph.explorer.api.services.graph import(
    DataLoaderBase,
    DataVisualizerBase
)
from sok.graph.explorer.api.model.graph import Graph,Node,Edge
import datetime


def index(request):
    # # Create a mock graph for demonstration
    # graph = Graph()

    # # Add 20 nodes to the graph
    # for i in range(1, 21):
    #     node = Node(i, data={"label": datetime.datetime.now()})
    #     graph.add_node(node)

    # # Add edges to connect the nodes
    # edges = [
    #     Edge(1, 2, ""),
    #     Edge(2, 3, ""),
    #     Edge(3, 4, ""),
    #     Edge(4, 5, ""),
    #     Edge(5, 6, ""),
    #     Edge(6, 7,""),
    #     Edge(7, 8, ""),
    #     Edge(8, 9, ""),
    #     Edge(9, 10, ""),
    #     Edge(10, 11,""),
    #     Edge(11, 12, ""),
    #     Edge(12, 13, ""),
    #     Edge(13, 14, ""),
    #     Edge(14, 15, ""),
    #     Edge(15, 16, ""),
    #     Edge(16, 17, ""),
    #     Edge(17, 18, ""),
    #     Edge(18, 19,""),
    #     Edge(19, 20, "") # Closing the loop
    # ]

    # for edge in edges:
    #     graph.add_edge(edge)
    test_data_path = Path("test.xml")

    plugin = apps.get_app_config('graph_explorer_platform').data_source_plugins[0]
    params = {
        'file_path': str(test_data_path),
        'directed': True
    }
    graph = plugin.load_graph(params)

    # Convert graph data to JSON-friendly format
    # graph_data = {
    #     "nodes": [{"id": node.id, "label": f"Node {node.id}"} for node in graph.nodes.values()],
    #     "links": [{"source": edge.source, "target": edge.target, "name": edge.name} for edge in graph.edges]
    # }
    
    simple_visualizer=apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
    graph_data={"code":''}
    graph_data["code"]=simple_visualizer.visualize_graph(graph)
    # print(graph_data['code'],apps.get_app_config('graph_explorer_platform').data_visalizer_plugins)
    return render(request, 'main.html', graph_data)
