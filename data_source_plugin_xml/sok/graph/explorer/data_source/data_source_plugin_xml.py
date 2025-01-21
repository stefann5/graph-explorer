from pathlib import Path
from typing import Any, Dict, List, Optional
from sok.graph.explorer.api.model.graph import Edge, Graph, Node
from sok.graph.explorer.api.services.graph import DataLoaderBase
import xml.etree.ElementTree as ET

class DataSourcePluginXml(DataLoaderBase):
    def __init__(self):
        self.element_to_id = {}
        self.processed_elements = set()
        self.parent_map = {}
        self.reference_elements = []  # Store (element, parent_element) tuples

    def identifier(self):
        return "DataSourcePluginXml"

    def name(self):
        return "Data Source Plugin XML"

    def get_required_params(self) -> List[str]:
        return ['file_path']

    def validate_input_params(self, params: Dict[str, Any]) -> bool:
        return all(param in params for param in self.get_required_params())

    def _build_parent_map(self, element: ET.Element, parent: Optional[ET.Element] = None):
        self.parent_map[element] = parent
        for child in element:
            if child.tag is not None:
                self._build_parent_map(child, element)

    def _get_element_siblings(self, element: ET.Element) -> List[ET.Element]:
        parent = self.parent_map.get(element)
        if parent is None:
            return [element]
        return [child for child in parent if child.tag == element.tag]

    def _create_element_path(self, element: ET.Element, parent_path: str = "") -> str:
        tag_with_index = element.tag
        siblings = self._get_element_siblings(element)
        if len(siblings) > 1:
            position = siblings.index(element) + 1
            tag_with_index = f"{element.tag}[{position}]"

        return f"{parent_path}/{tag_with_index}" if parent_path else tag_with_index

    def _resolve_reference(self, reference: str, current_element: ET.Element) -> Optional[ET.Element]:
        try:
            current = current_element
            parts = reference.split('/')

            while parts and parts[0] == '..':
                current = self.parent_map.get(current)
                if current is None:
                    return None
                parts.pop(0)

            for part in parts:
                if not part:
                    continue

                if '[' in part:
                    tag, index = part[:-1].split('[')
                    index = int(index)
                    siblings = [child for child in current if child.tag == tag]
                    if 0 < index <= len(siblings):
                        current = siblings[index - 1]
                    else:
                        return None
                else:
                    found = False
                    for child in current:
                        if child.tag == part:
                            current = child
                            found = True
                            break
                    if not found:
                        return None

            return current
        except Exception:
            return None

    def _first_pass_process(self, element: ET.Element, parent_path: str = "") -> None:
        current_path = self._create_element_path(element, parent_path)

        if current_path not in self.element_to_id:
            current_id = element.attrib.get('id')
            self.element_to_id[current_path] = current_id

            # Store reference elements with their parent element
            if 'reference' in element.attrib:
                parent = self.parent_map.get(element)
                if parent is not None:
                    self.reference_elements.append((element, parent))

            for child in element:
                if child.tag is not None:
                    self._first_pass_process(child, current_path)

    def _create_graph_structure(self, element: ET.Element, graph: Graph, parent_id: Optional[int] = None,
                                parent_path: str = "") -> None:
        current_path = self._create_element_path(element, parent_path)
        current_id = self.element_to_id[current_path]

        # Handle references later in _process_references
        if 'reference' in element.attrib:
            return

        # Check if the element has children
        if len(list(element)) == 0:  # Treat as an attribute if no children
            if parent_id is not None:
                parent_node = graph.get_node(parent_id)
                if parent_node is not None:
                    # Add this element as an attribute to the parent
                    attributes = parent_node.data.get('attributes', {})
                    attributes[element.tag] = element.text.strip() if element.text else ''
                    parent_node.data['attributes'] = attributes
            return  # Skip further processing for this element

        # Process as a normal node if it has children
        node_data = {
            'tag': element.tag,
            'text': element.text.strip() if element.text else '',
            'path': current_path,
            'attributes': {k: v for k, v in element.attrib.items() if k != 'reference'}  # Handle XML attributes
        }
        node = Node(current_id, node_data)
        graph.add_node(node)

        if parent_id is not None:
            edge = Edge(parent_id, current_id, "parent_child")
            graph.add_edge(edge)

        # Recursively process child elements
        for child in element:
            if child.tag is not None:
                self._create_graph_structure(child, graph, current_id, current_path)

    def _process_references(self, graph: Graph):
        """Process all stored references after graph structure is created."""
        for element, parent_element in self.reference_elements:
            reference = element.get('reference')
            referenced_element = self._resolve_reference(reference, element)

            if referenced_element is not None:
                # Get path for parent element
                parent_chain = []
                current = parent_element
                while current is not None:
                    parent_chain.insert(0, current)
                    current = self.parent_map.get(current)

                # Build parent path
                parent_path = ""
                for p in parent_chain:
                    parent_path = self._create_element_path(p, parent_path)

                # Get path for referenced element
                ref_chain = []
                current = referenced_element
                while current is not None:
                    ref_chain.insert(0, current)
                    current = self.parent_map.get(current)

                # Build referenced path
                ref_path = ""
                for r in ref_chain:
                    ref_path = self._create_element_path(r, ref_path)

                if parent_path in self.element_to_id and ref_path in self.element_to_id:
                    parent_id = self.element_to_id[parent_path]
                    referenced_id = self.element_to_id[ref_path]
                    edge = Edge(parent_id, referenced_id, "references")
                    graph.add_edge(edge)

    def parse_file(self, file_path: str) -> Graph:
        graph = Graph(directed=True)

        tree = ET.parse(file_path)
        root = tree.getroot()

        # Reset state
        self.node_id_counter = 0
        self.element_to_id.clear()
        self.processed_elements.clear()
        self.parent_map.clear()
        self.reference_elements.clear()

        # Build parent map
        self._build_parent_map(root)

        # First pass: Build element_to_id mapping
        self._first_pass_process(root)

        # Second pass: Create graph structure
        self._create_graph_structure(root, graph)

        # Third pass: Process references
        self._process_references(graph)

        if len(graph.nodes) > 200:
            raise ValueError(f"Generated graph has {len(graph.nodes)} nodes. Maximum allowed is 200.")

        return graph

    def load_graph(self, params: Dict[str, Any]) -> Graph:
        if not self.validate_input_params(params):
            raise ValueError(f"Missing required parameters. Required: {self.get_required_params()}")

        file_path = params['file_path']
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        return self.parse_file(file_path)