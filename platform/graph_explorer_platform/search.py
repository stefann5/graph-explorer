from datetime import datetime
from typing import Any
from sok.graph.explorer.api.model.graph import Graph
from sok.graph.explorer.api.services.graph import ServiceBase


class GraphSearchFilter(ServiceBase):
    def identifier(self):
        return "graph_search_filter"

    def name(self):
        return "Graph Search and Filter"

    def _compare_values(self, value1: Any, value2: Any, operator: str) -> bool:
        """Compare two values using the specified operator."""
        if type(value1) != type(value2):
            try:
                # Try to convert value1 to the type of value2
                value1 = type(value2)(value1)
            except (ValueError, TypeError):
                raise ValueError(f"Cannot compare values of different types: {type(value1)} and {type(value2)}")

        if operator == "==":
            return value1 == value2
        elif operator == "!=":
            return value1 != value2
        elif operator == ">":
            return value1 > value2
        elif operator == ">=":
            return value1 >= value2
        elif operator == "<":
            return value1 < value2
        elif operator == "<=":
            return value1 <= value2
        else:
            raise ValueError(f"Invalid operator: {operator}")

    def search(self, graph: Graph, query: str) -> Graph:
        """
        Search the graph for nodes containing the query string in their attributes.
        Returns a new subgraph containing matching nodes and their connections.
        """
        if not query:
            return graph

        date = False
        if isinstance(self._convert_value(query), datetime):
            query += " 00:00:00"
            date = True

        # Create new graph with same directedness
        result_graph = Graph(directed=graph.directed)

        # Find matching nodes
        matching_nodes = []
        for node_id, node in graph.nodes.items():
            for attr_name, attr_value in node.data.items():
                if query.lower() in str(attr_name).lower() or query.lower() in str(attr_value).lower():
                    if not date:
                        matching_nodes.append(node_id)
                        break
                if date and isinstance(attr_value, dict) and 'date' in attr_value:
                    if str(attr_value['date']) == query:
                        matching_nodes.append(node_id)
                        break

        # Add matching nodes to result graph
        for node_id in matching_nodes:
            result_graph.add_node(graph.get_node(node_id))

        # Add edges between matching nodes
        for edge in graph.edges:
            if edge.source in matching_nodes and edge.target in matching_nodes:
                result_graph.add_edge(edge)

        return result_graph

    def _convert_value(self, value: Any) -> Any:
        """Convert value to appropriate type."""
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                try:
                    return int(value)
                except ValueError:
                    try:
                        return float(value)
                    except ValueError:
                        return value
        return value

    def filter(self, graph: Graph, filter_query: str) -> Graph:
        """
        Filter the graph based on the query in format: <attribute_name> <operator> <value>
        Returns a new subgraph containing matching nodes and their connections.
        """
        # Parse filter query
        parts = filter_query.split()
        if len(parts) != 3:
            raise ValueError("Filter query must be in format: <attribute_name> <operator> <value>")

        attr_name, operator, value = parts

        value = self._convert_value(value)
        if isinstance(value, datetime):
            value = value.replace(hour=0, minute=0)

        if operator not in ["==", "!=", ">", ">=", "<", "<="]:
            raise ValueError(f"Invalid operator: {operator}")

        # Create new graph with same directedness
        result_graph = Graph(directed=graph.directed)

        # Find matching nodes
        matching_nodes = []
        for node_id, node in graph.nodes.items():
            if attr_name in node.data['attributes']:
                node_value = node.data['attributes'][attr_name]
                try:
                    if self._compare_values(node_value, value, operator):
                        matching_nodes.append(node_id)
                except ValueError as e:
                    raise ValueError(f"Type mismatch for node {node_id}: {str(e)}")

        # Add matching nodes to result graph
        for node_id in matching_nodes:
            result_graph.add_node(graph.get_node(node_id))

        # Add edges between matching nodes
        for edge in graph.edges:
            if edge.source in matching_nodes and edge.target in matching_nodes:
                result_graph.add_edge(edge)

        return result_graph