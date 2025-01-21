import json
from pathlib import Path
from datetime import datetime
from data_source_plugin_json import JsonDataSourcePlugin

# Test data with various types and cyclic references
test_data = {
    "@id": "root",
    "name": "Company",
    "founded_date": "2024-01-20",
    "employee_count": 100,
    "revenue": 1500000.50,
    "departments": [
        {
            "@id": "dept1",
            "name": "Engineering",
            "manager": {
                "@id": "emp1",
                "name": "John Smith",
                "department": "dept1"  # Cyclic reference
            }
        },
        {
            "@id": "dept2",
            "name": "Marketing",
            "manager": {
                "@id": "emp2",
                "name": "Jane Doe",
                "department": "dept2"  # Cyclic reference
            }
        }
    ],
    "main_dept": "dept1"  # Reference by ID
}

def test_json_plugin():
    # Save the test data to a file
    test_data_path = Path("test_data.json")
    with open(test_data_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=2)

    # Test both directed and undirected graphs
    for directed in [True, False]:
        print(f"\nTesting {'directed' if directed else 'undirected'} graph:")
        
        # Create and run the plugin
        plugin = JsonDataSourcePlugin()
        params = {
            'file_path': str(test_data_path),
            'directed': directed
        }
        
        try:
            # Process the data
            graph = plugin.load_graph(params)
            
            # Print statistics
            print(f"Total nodes: {len(graph.nodes)}")
            print(f"Total edges: {len(graph.edges)}")
            
            # Print all nodes and their data
            print("\nNodes:")
            for node_id, node in graph.nodes.items():
                print(f"Node {node_id}: {node.data}")
            
            # Print all edges
            print("\nEdges:")
            for edge in graph.edges:
                source_node = graph.nodes[edge.source]
                target_node = graph.nodes[edge.target]
                print(f"Edge {edge.name}: {source_node.data.get('name', 'Unknown')} -> {target_node.data.get('name', 'Unknown')}")
            
            # Verify types
            print("\nVerifying data types:")
            for node in graph.nodes.values():
                for key, value in node.data.items():
                    print(f"Node attribute '{key}' is of type: {type(value)}")
            
        except Exception as e:
            print(f"Error occurred: {e}")
            raise
        
    # Clean up
    test_data_path.unlink()

if __name__ == "__main__":
    test_json_plugin()