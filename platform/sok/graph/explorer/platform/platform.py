from typing import List, Union
from importlib.metadata import entry_points

from sok.graph.explorer.api.services.graph import(
    DataLoaderBase,
    DataVisualizerBase
)

def load_plugins(label):
    """
    Dinamicko prepoznavanje plagina na osnovu pripadajuce grupe.
    """
    plugins = []
    for ep in entry_points(group=label):
        # Ucitavanje plagina.
        p = ep.load()
        print(f"{ep.name} {p}")
        # instanciranje odgovarajuce klase
        plugin = p()
        plugins.append(plugin)
    return plugins

def main():
    print("asds")
    try:
        data_source_plugins = load_plugins("graph.data_source")
        data_visalizer_plugins = load_plugins("graph.data_visualizer")

    except Exception as e:
        print(f"Error: {e}")
        return
    
if __name__ == "__main__":
    main()