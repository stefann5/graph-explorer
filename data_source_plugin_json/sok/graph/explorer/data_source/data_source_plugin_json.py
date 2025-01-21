from typing import Dict, Any, Set, Union, Optional
from sok.graph.explorer.api.model.graph import Graph,Node,Edge
from sok.graph.explorer.api.services.graph import DataLoaderBase
from datetime import datetime
import json
from pathlib import Path
import uuid

class JsonDataSourcePlugin(DataLoaderBase):
    def identifier(self):
        return "DataSourceJson"

    def name(self):
        return "Data Source Json"
    
    def __init__(self):
        self.graph = None
        self.id_map: Dict[str, int] = {}  # Maps JSON @id to node id
        self.current_id = 0

    def get_next_id(self) -> int:
        """Generate next unique ID for nodes."""
        self.current_id += 1
        return self.current_id

    def parse_file(self, file_path: Union[str, Path], directed: bool = True) -> Graph:
        """Parse JSON file and create a graph."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return self.parse_data(data, directed)

    def _convert_value(self, value: Any) -> Any:
        """Convert value to appropriate type."""
        if isinstance(value, str):
            # Try to parse as date
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return value
        return value

    def parse_data(self, data: Any, directed: bool = True) -> Graph:
        """Parse JSON data and create a graph."""
        self.graph = Graph(directed=directed)
        self.id_map.clear()
        self.current_id = 0

        # First pass: Create all nodes
        self._create_nodes(data)
        
        # Second pass: Create all edges
        self._create_edges(data)
        
        return self.graph

    def _create_nodes(self, data: Any, parent_path: str = ""):
        """First pass: Create nodes for all objects."""
        if not isinstance(data, dict):
            return

        # Get or create node ID
        node_id = None
        if "@id" in data:
            if data["@id"] in self.id_map:
                return
            node_id = self.get_next_id()
            self.id_map[data["@id"]] = node_id
        else:
            node_id = self.get_next_id()
            
        # Create node with non-object attributes
        node_data = {}
        for key, value in data.items():
            if key != "@id" and not isinstance(value, (dict, list)):
                node_data[key] = self._convert_value(value)
        
        self.graph.add_node(Node(node_id, node_data))

        # Process nested objects
        for key, value in data.items():
            if isinstance(value, dict):
                self._create_nodes(value, f"{parent_path}.{key}")
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._create_nodes(item, f"{parent_path}.{key}[]")

    def _create_edges(self, data: Any, parent_path: str = ""):
        """Second pass: Create edges for object references and attributes."""
        if not isinstance(data, dict):
            return

        current_id = self.id_map.get(data.get("@id")) or self.get_next_id()

        for key, value in data.items():
            if key == "@id":
                continue

            if isinstance(value, dict):
                # Create edge to nested object
                if "@id" in value:
                    target_id = self.id_map[value["@id"]]
                    self.graph.add_edge(Edge(current_id, target_id, key))
                self._create_edges(value, f"{parent_path}.{key}")
            
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        if "@id" in item:
                            target_id = self.id_map[item["@id"]]
                            self.graph.add_edge(Edge(current_id, target_id, f"{key}[{i}]"))
                        self._create_edges(item, f"{parent_path}.{key}[]")
            
            elif isinstance(value, str) and value in self.id_map:
                # Create edge for string reference to another object
                target_id = self.id_map[value]
                self.graph.add_edge(Edge(current_id, target_id, key))

    def validate_input_params(self, params: Dict[str, Any]) -> bool:
        """Validate input parameters for the plugin."""
        required_params = {'file_path', 'directed'}
        return all(param in params for param in required_params)

    def get_required_params(self) -> Dict[str, str]:
        """Return dictionary of required parameters and their descriptions."""
        return {
            'file_path': 'Path to the JSON file to be parsed',
            'directed': 'Boolean indicating if the graph should be directed (True/False)'
        }

    def load_graph(self, params: Dict[str, Any]) -> Graph:
        """Main processing method for the plugin."""
        if not self.validate_input_params(params):
            raise ValueError(f"Missing required parameters. Required: {self.get_required_params()}")
        
        file_path = params['file_path']
        directed = params['directed']
        
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return self.parse_file(file_path, directed)