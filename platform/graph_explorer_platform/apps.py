from importlib.metadata import entry_points
from django.apps import AppConfig
import pkg_resources

class GraphExplorerPlatformConfig(AppConfig):
    name = 'graph_explorer_platform'
    data_source_plugins = []
    selected_plugin = None
    data_source = None
    data_visalizer_plugins = []

    def ready(self):
        self.data_source_plugins = load_plugins("graph.data_source")
        self.data_visalizer_plugins = load_plugins("graph.data_visualizer")
        
        if len(self.data_source_plugins) > 0:
            self.selected_plugin = self.data_source_plugins[0]
            if 'json' in self.data_source_plugins[0].__class__.__name__.lower():
                self.data_source = 'test.json'
            if 'xml' in self.data_source_plugins[0].__class__.__name__.lower():
                self.data_source = 'test.xml'

    def set_data_source_plugin(self, plugin_type):
        """
        Set the active data source plugin based on type string (xml/json)
        Returns True if successful, False if plugin type not found
        """
        plugin_type = plugin_type.lower()
        for plugin in self.data_source_plugins:
            # Check class name for matching type
            class_name = plugin.__class__.__name__.lower()
            if plugin_type in class_name:               
                self.selected_plugin = plugin
                if(plugin_type == 'jsondatasourceplugin'):
                    self.data_source = 'test.json'
                if(plugin_type == 'datasourcepluginxml'):
                    self.data_source = 'test.xml'
                return True
        return False
    
    def set_file(self, file):
        if file != '':
            self.data_source = file
    
        
    def get_current_plugin(self):
            """Return currently selected plugin"""
            return self.selected_plugin

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