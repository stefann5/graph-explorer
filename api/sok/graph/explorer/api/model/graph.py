from typing import Dict, List, Optional, Any

class Node:
    def __init__(self, id: int, data: Dict[str, Any] = None):
        self.id = id
        self.data = data or {}

    def __str__(self):
        return f"ID: {self.id} Data: {self.data}"

    def __repr__(self):
        return f"Node(id={self.id}, data={self.data})"

class Edge:
    def __init__(self, source: int, target: int, name: str = ""):
        self.source = source
        self.target = target
        self.name = name

    def __str__(self):
        return f"Source Node ID: {self.source} Target Node ID: {self.target} Edge Name: {self.name}"

    def __repr__(self):
        return f"Edge(source={self.source}, target={self.target}, name='{self.name}')"

class Graph:
    def __init__(self, directed: bool = False):
        self.nodes: Dict[int, Node] = {}
        self.edges: List[Edge] = []
        self.directed = directed
        self.adjacency_list: Dict[int, List[int]] = {}

    def add_node(self, node: Node):
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.adjacency_list[node.id] = []

    def add_edge(self, edge: Edge):
        if edge.source not in self.nodes:
            raise ValueError(f"Source node {edge.source} does not exist")
        if edge.target not in self.nodes:
            raise ValueError(f"Target node {edge.target} does not exist")

        self.edges.append(edge)
        self.adjacency_list[edge.source].append(edge.target)
        
        if not self.directed:
            reverse_edge = Edge(edge.target, edge.source, edge.name)
            self.adjacency_list[edge.target].append(edge.source)

    def get_node(self, node_id: int) -> Optional[Node]:
        return self.nodes.get(node_id)

    def get_edges_for_node(self, node_id: int) -> List[Edge]:
        return [edge for edge in self.edges if edge.source == node_id or (not self.directed and edge.target == node_id)]

    def get_neighbors(self, node_id: int) -> List[int]:
        return self.adjacency_list.get(node_id, [])

    def remove_node(self, node_id: int):
        if node_id not in self.nodes:
            return

        del self.nodes[node_id]
        del self.adjacency_list[node_id]

        self.edges = [
            edge for edge in self.edges 
            if edge.source != node_id and edge.target != node_id
        ]

        for node in self.adjacency_list:
            self.adjacency_list[node] = [
                neighbor for neighbor in self.adjacency_list[node] 
                if neighbor != node_id
            ]

    def __str__(self):
        node_str = "\nNodes:\n" + "\n".join(str(node) for node in self.nodes.values())
        edge_str = "\n\nEdges:\n" + "\n".join(str(edge) for edge in self.edges)
        return node_str + edge_str