
import json
import logging
import os
from pathlib import Path
from django.shortcuts import render
import xml.etree.ElementTree as ET
from django.apps.registry import apps
from django.views.decorators.csrf import csrf_exempt
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
    graph=apps.get_app_config('graph_explorer_platform').graph
    simple_visualizer=apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
    graph_data={"code":''}
    graph_data["code"]=simple_visualizer.visualize_graph(apps.get_app_config('graph_explorer_platform').graph)
    return render(request, 'main.html', graph_data)


def delete_node(request):
    if request.method == 'POST':
        try:
            # Parsiranje tela zahteva
            body = json.loads(request.body)
            node_id = body.get('id')

            if node_id is None:
                return JsonResponse({"message": "Node ID is required."}, status=400)

            if isinstance(node_id, list):
                node_id = node_id[0]  # Uzmi prvi element liste

                # Uveri se da je node_id zaista broj
            try:
                node_id = int(node_id)
            except ValueError:
                return JsonResponse({"message": "Node ID must be an integer."}, status=400)

            # Učitavanje grafa iz izvora podataka
            test_data_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
            plugin = apps.get_app_config('graph_explorer_platform').selected_plugin
            params = {
                'file_path': str(test_data_path),
                'directed': True
            }
            apps.get_app_config('graph_explorer_platform').graph = plugin.load_graph(params)
            graph = apps.get_app_config('graph_explorer_platform').graph
            print(graph.nodes)

            # Provera da li čvor postoji
            if not graph.get_node(node_id):
                return JsonResponse({"message": "Node does not exist."}, status=400)

            # Provera da li čvor ima povezane grane
            connected_edges = graph.get_edges_for_node(node_id)
            if connected_edges:
                graph.edges = [edge for edge in graph.edges if edge not in connected_edges]

                #return JsonResponse(
                   # {"message": "Edges connected to the node were deleted first. Please try deleting the node again."},
                  #  status=400)

            # Brisanje čvora
            graph.remove_node(node_id)
            print(graph.nodes)
            print(graph.edges)

            # Osvježavanje vizualizacije
            simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
            visualization_js = simple_visualizer.visualize_graph(graph)

            return JsonResponse({"message": "Node deleted successfully.", "visualization_js": visualization_js},
                                status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=405)


@csrf_exempt
def update_node(request):
    if apps.get_app_config('graph_explorer_platform').data_source == 'test.xml':
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                node_id = body.get('id')
                data = body.get('data', {})

                # Load the XML file
                xml_file_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
                if not xml_file_path.exists():
                    return JsonResponse({"message": "XML file not found."}, status=404)

                tree = ET.parse(xml_file_path)
                root = tree.getroot()

                # Find the node to update
                node = root.find(f".//*[@id='{node_id}']")
                if node is None:
                    return JsonResponse({"message": "Node not found in the XML file."}, status=404)

                # Update node attributes
                for key, value in data.items():
                    child = node.find(key)
                    if child is not None:
                        child.text = str(value)
                    else:
                        new_child = ET.SubElement(node, key)
                        new_child.text = str(value)

                # Save the updated XML file
                tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)

                # Reload the graph
                xml_file_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
                plugin = apps.get_app_config('graph_explorer_platform').selected_plugin
                params = {'file_path': str(xml_file_path), 'directed': True}
                apps.get_app_config('graph_explorer_platform').graph = plugin.load_graph(params)
                graph = apps.get_app_config('graph_explorer_platform').graph

                # Visualize the updated graph
                simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
                visualization_js = simple_visualizer.visualize_graph(graph)

                return JsonResponse({
                    "message": "Node updated successfully.",
                    "visualization_js": visualization_js
                }, status=200)
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=500)

        return JsonResponse({"message": "Invalid request method."}, status=405)
    else:
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                node_id = body.get('id')
                data = body.get('data', {})

                # Load the JSON file
                test_data_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
                if not test_data_path.exists():
                    return JsonResponse({"message": "JSON file not found."}, status=404)

                with open(test_data_path, 'r', encoding='utf-8') as file:
                    json_data = json.load(file)

                # Update the node in the JSON structure
                def update_node_data(node_list, node_id, data):
                    for node in node_list:
                        if node.get('@id') == node_id:
                            node.update(data)
                            return True
                        if 'children' in node:
                            if update_node_data(node['children'], node_id, data):
                                return True
                    return False

                if not update_node_data(json_data['children'], node_id, data):
                    return JsonResponse({"message": "Node not found."}, status=404)

                # Save the updated JSON structure back to the file
                with open(test_data_path, 'w', encoding='utf-8') as file:
                    json.dump(json_data, file, indent=4, ensure_ascii=False)

                # Reload the graph
                test_data_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
                plugin = apps.get_app_config('graph_explorer_platform').selected_plugin
                params = {'file_path': str(test_data_path), 'directed': True}
                apps.get_app_config('graph_explorer_platform').graph = plugin.load_graph(params)
                graph = apps.get_app_config('graph_explorer_platform').graph

                # Visualize the updated graph
                simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
                visualization_js = simple_visualizer.visualize_graph(graph)

                return JsonResponse({
                    "message": "Node updated successfully.",
                    "visualization_js": visualization_js
                }, status=200)
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=500)

        return JsonResponse({"message": "Invalid request method."}, status=405)

@csrf_exempt
def add_node(request):
    if apps.get_app_config('graph_explorer_platform').data_source=='test.xml':
        if request.method == 'POST':
            try:
                # Parse the request body
                body = json.loads(request.body)
                node_id = body.get('id')
                data = body.get('data', {})

                # Load the XML file
                xml_file_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
                if not xml_file_path.exists():
                    return JsonResponse({"message": "XML file not found."}, status=404)

                tree = ET.parse(xml_file_path)
                root = tree.getroot()

                # Check if node with this ID already exists
                if root.find(f".//*[@id='{node_id}']") is not None:
                    return JsonResponse({"message": "Node with this ID already exists in the XML file."}, status=400)

                # Find the parent node if specified
                parent_id = data.get('parent')
                parent_node = None
                if parent_id:
                    parent_node = root.find(f".//*[@id='{parent_id}']")
                    if parent_node is None:
                        return JsonResponse({"message": "Parent node not found in the XML file."}, status=400)

                # Create the new node
                new_node = ET.Element("Person", id=str(node_id))
                for key, value in data.items():
                    if isinstance(value, dict):
                        child_element = ET.SubElement(new_node, key)
                        for sub_key, sub_value in value.items():
                            sub_element = ET.SubElement(child_element, sub_key)
                            sub_element.text = str(sub_value)
                    else:
                        child_element = ET.SubElement(new_node, key)
                        child_element.text = str(value)

                # Add the new node to the parent or root
                if parent_node is not None:
                    parent_node.append(new_node)
                else:
                    root.append(new_node)

                # Save the updated XML file
                tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)

                # Update the graph
                xml_file_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
                plugin = apps.get_app_config('graph_explorer_platform').selected_plugin
                params = {
                    'file_path': str(xml_file_path),
                    'directed': True
                }
                apps.get_app_config('graph_explorer_platform').graph = plugin.load_graph(params)
                graph = apps.get_app_config('graph_explorer_platform').graph

                # Add the new node to the graph
                data['attributes'] = data.copy()
                new_node = Node(node_id, data=data)  # Assuming Node takes id and additional attributes
                graph.add_node(new_node)

                # Visualize the updated graph
                simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
                visualization_js = simple_visualizer.visualize_graph(graph)

                return JsonResponse({
                    "message": "Node added successfully.",
                    "visualization_js": visualization_js
                }, status=200)
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=500)

        return JsonResponse({"message": "Invalid request method."}, status=405)
    else:
        if request.method == 'POST':
            try:
                # Parse the request body
                body = json.loads(request.body)
                node_id = body.get('id')
                data = body.get('data', {})

                # Load the current graph using the data source plugin
                test_data_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
                # Update the JSON file
                if test_data_path.exists():
                    with open(test_data_path, 'r', encoding='utf-8') as file:
                        json_data = json.load(file)

                    def node_exists(node_list, node_id):
                        for node in node_list:
                            if node.get('@id') == node_id:
                                return True
                            if 'children' in node:
                                if node_exists(node['children'], node_id):
                                    return True
                        return False

                    # Proveriti da li već postoji čvor sa istim ID-jem
                    if node_exists(json_data['children'], node_id):
                        return JsonResponse({"message": "Node with this ID already exists in the JSON file."}, status=400)

                    # Traverse and find the parent node to which the new node should be added
                    parent_id = data.get('parent')
                    if parent_id:
                        def add_child_to_parent(node_list, parent_id, new_child):
                            for node in node_list:
                                if node.get('@id') == parent_id:
                                    if 'children' not in node:
                                        node['children'] = []
                                    node['children'].append(new_child)
                                    return True
                                if 'children' in node:
                                    if add_child_to_parent(node['children'], parent_id, new_child):
                                        return True
                            return False

                        # Define the new child node structure
                        new_child = {
                            "@id": node_id,
                            **data  # Add all additional attributes provided
                        }

                        if not add_child_to_parent(json_data['children'], parent_id, new_child):
                            return JsonResponse({"message": "Parent node not found."}, status=400)
                    else:
                        # If no parent is specified, add the node at the top level
                        json_data['children'].append({
                            "@id": node_id,
                            **data
                        })

                    # Save the updated JSON structure back to the file
                    with open(test_data_path, 'w', encoding='utf-8') as file:
                        json.dump(json_data, file, indent=4, ensure_ascii=False)

                test_data_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
                plugin = apps.get_app_config('graph_explorer_platform').selected_plugin
                params = {
                    'file_path': str(test_data_path),
                    'directed': True
                }
                apps.get_app_config('graph_explorer_platform').graph = plugin.load_graph(params)
                graph=apps.get_app_config('graph_explorer_platform').graph

                # Add the new node to the graph
               # if node_id in graph.nodes:
                #    return JsonResponse({"message": "Node already exists."}, status=400)

                data['attributes'] = data.copy()
                new_node = Node(node_id, data=data)  # Assuming Node takes id and additional attributes
                graph.add_node(new_node)

                # Visualize the updated graph
                simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
                visualization_js = simple_visualizer.visualize_graph(graph)

                return JsonResponse({
                    "message": "Node added successfully.",
                    "visualization_js": visualization_js
                }, status=200)
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=500)

        return JsonResponse({"message": "Invalid request method."}, status=405)

@csrf_exempt
def add_edge(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            source = body.get('source')
            target = body.get('target')
            name = body.get('name', '')

            test_data_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
            plugin = apps.get_app_config('graph_explorer_platform').selected_plugin
            params = {
                'file_path': str(test_data_path),
                'directed': True
            }
            apps.get_app_config('graph_explorer_platform').graph = plugin.load_graph(params)
            graph = apps.get_app_config('graph_explorer_platform').graph
            if not graph.get_node(source) or not graph.get_node(target):
                return JsonResponse({"message": "Source or target node does not exist."}, status=400)

            edge = Edge(source, target, name)
            graph.add_edge(edge)

            simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
            visualization_js = simple_visualizer.visualize_graph(graph)
            print(graph.edges)

            return JsonResponse({"message": "Edge added successfully.", "visualization_js": visualization_js}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=405)


@csrf_exempt
def update_edge(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            source = body.get('source')
            target = body.get('target')
            name = body.get('name', '')

            test_data_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
            plugin = apps.get_app_config('graph_explorer_platform').selected_plugin
            params = {
                'file_path': str(test_data_path),
                'directed': True
            }
            apps.get_app_config('graph_explorer_platform').graph = plugin.load_graph(params)
            graph = apps.get_app_config('graph_explorer_platform').graph

            for edge in graph.edges:
                if str(edge.source) == str(source) and str(edge.target) == str(target):
                    edge.name = name
                    break
            else:
                return JsonResponse({"message": "Edge not found."}, status=404)

            simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
            visualization_js = simple_visualizer.visualize_graph(graph)
            print(graph.edges)
            return JsonResponse({"message": "Edge updated successfully.", "visualization_js": visualization_js}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=405)

@csrf_exempt
def delete_edge(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            source = body.get('source')
            target = body.get('target')

            test_data_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
            plugin = apps.get_app_config('graph_explorer_platform').selected_plugin
            params = {
                'file_path': str(test_data_path),
                'directed': True
            }
            apps.get_app_config('graph_explorer_platform').graph = plugin.load_graph(params)
            graph = apps.get_app_config('graph_explorer_platform').graph

            graph.edges = [edge for edge in graph.edges if not (edge.source == source and edge.target == target)]

            simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
            visualization_js = simple_visualizer.visualize_graph(graph)
            print(graph.edges)

            return JsonResponse({"message": "Edge deleted successfully.", "visualization_js": visualization_js}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=405)

@csrf_exempt
def delete_graph(request):
    if request.method == 'POST':
        try:
            # Pronađi plugin za graf i učitaj trenutni graf
            test_data_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
            plugin = apps.get_app_config('graph_explorer_platform').selected_plugin
            params = {
                'file_path': str(test_data_path),
                'directed': True
            }
            apps.get_app_config('graph_explorer_platform').graph = plugin.load_graph(params)
            graph = apps.get_app_config('graph_explorer_platform').graph

            # Briši sve čvorove i ivice iz grafa
            graph.nodes.clear()
            graph.edges.clear()
            graph.adjacency_list.clear()

            # Generiši novu vizualizaciju
            simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
            visualization_js = simple_visualizer.visualize_graph(graph)

            return JsonResponse({"message": "Graph deleted successfully.", "visualization_js": visualization_js}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=405)

@csrf_exempt
def search_graph(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            query = body.get('query')
            query=query[0]
            test_data_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
            plugin = apps.get_app_config('graph_explorer_platform').selected_plugin
            params = {
                'file_path': str(test_data_path),
                'directed': True
            }
            apps.get_app_config('graph_explorer_platform').graph = plugin.load_graph(params)
            graph = apps.get_app_config('graph_explorer_platform').graph
            filter_service = GraphSearchFilter()
            graph = filter_service.search(graph,query)

            simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
            visualization_js = simple_visualizer.visualize_graph(graph)


            return JsonResponse({"message": "Search done successfully.", "visualization_js": visualization_js}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=405)

@csrf_exempt
def filter_graph(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            query = body.get('query')
            test_data_path = Path(apps.get_app_config('graph_explorer_platform').data_source)
            plugin = apps.get_app_config('graph_explorer_platform').selected_plugin
            params = {
                'file_path': str(test_data_path),
                'directed': True
            }
            apps.get_app_config('graph_explorer_platform').graph = plugin.load_graph(params)
            graph = apps.get_app_config('graph_explorer_platform').graph
            filter_service = GraphSearchFilter()
            graph = filter_service.filter(graph,query)

            simple_visualizer = apps.get_app_config('graph_explorer_platform').data_visalizer_plugins[0]
            visualization_js = simple_visualizer.visualize_graph(graph)


            return JsonResponse({"message": "Filter done successfully.", "visualization_js": visualization_js}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=405)


def select_plugin(request):
    if request.method == 'POST':
        query = request.POST.get('query', 1)
        apps.get_app_config('graph_explorer_platform').set_data_source_plugin(query)

    return index(request)

def select_file(request):
    if request.method == 'POST':
        file = request.POST.get('file', '')
        plugin_name = apps.get_app_config('graph_explorer_platform').selected_plugin.__class__.__name__.lower()

        if not os.path.exists(file):
            return JsonResponse({"message": "File does not exist!"}, status=400)

        if ('json' not in file and 'xml' not in file) or ('json' in plugin_name and 'xml' in file) or ('xml' in plugin_name and 'json' in file):
            return JsonResponse({"message": "Bad data source file path!"}, status=400)
        apps.get_app_config('graph_explorer_platform').set_file(file)
 
    return index(request)

def get_available_plugins(request):
    app_config = apps.get_app_config('graph_explorer_platform')
    
    # Extract plugin names for the select options
    data_source_plugins = [
        {
            'name': plugin.__class__.__name__
        } 
        for plugin in app_config.data_source_plugins
    ]

    context = {
        'data_source_plugins': data_source_plugins,
        'selected_plugin': app_config.selected_plugin.__class__.__name__ if app_config.selected_plugin else None
    }

    return JsonResponse(context)

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
    
def toggle_view(request):
    if request.method == 'POST':
        view_type = request.POST.get('view_type', 'simple')
        app_config = apps.get_app_config('graph_explorer_platform')
        
        if view_type == 'simple':
            visualizer = app_config.data_visalizer_plugins[0]
        else:
            if len(app_config.data_visalizer_plugins) > 1:
                visualizer = app_config.data_visalizer_plugins[1]
            else:
                visualizer = app_config.data_visalizer_plugins[0]
        graph_data = {"code": visualizer.visualize_graph(app_config.graph)}
        return JsonResponse(graph_data)
    return JsonResponse({"error": "Invalid request"}, status=400)