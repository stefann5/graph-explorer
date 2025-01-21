# Example XML file path (replace with your actual file path)
from pathlib import Path

from data_source_plugin_xml import DataSourcePluginXml



xml_file = Path("test.xml")

# Create the plugin instance
plugin = DataSourcePluginXml()

# Parameters dictionary with the file path
params = {'file_path': str(xml_file)}

# Load the graph
graph = plugin.load_graph(params)

# Print the graph nodes and edges
print("Graph Nodes:")
for node in graph.nodes.values():
    print(node)

print("\nGraph Edges:")
for edge in graph.edges:
    print(edge)