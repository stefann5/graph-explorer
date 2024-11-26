from sok.graph.explorer.api.model.graph import Graph
from sok.graph.explorer.api.services.graph import DataVisualizerBase

class SimpleVisualizer(DataVisualizerBase):
    def identifier(self):
        return "SimpleVisualizer"

    def name(self):
        return "Simple graph visualizer"
    
    def visualize_graph(self, graph: Graph):
        return "simply visalizing"