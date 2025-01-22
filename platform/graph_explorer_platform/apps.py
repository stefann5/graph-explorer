from importlib.metadata import entry_points
from django.apps import AppConfig
import pkg_resources

class GraphExplorerPlatformConfig(AppConfig):
    name = 'graph_explorer_platform'
    data_source_plugins = []
    data_visalizer_plugins = []
    def ready(self):
        self.data_source_plugins = load_plugins("graph.data_source")
        self.data_visalizer_plugins = load_plugins("graph.data_visualizer")
    graph=None

def load_plugins(label):
    plugins = []
    for ep in entry_points(group=label):
        # Ucitavanje plagina.
        p = ep.load()
        # instanciranje odgovarajuce klase
        plugin = p()
        plugins.append(plugin)
    return plugins
