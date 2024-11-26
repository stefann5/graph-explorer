from sok.graph.explorer.api.model.graph import Graph
from sok.graph.explorer.api.services.graph import DataVisualizerBase

class BlockVisualizer(DataVisualizerBase):
    def identifier(self):
        return "BlockVisualizer"

    def name(self):
        return "Block graph visualizer"
    
    def visualize_graph(self, graph: Graph):
        return "block visalizing"