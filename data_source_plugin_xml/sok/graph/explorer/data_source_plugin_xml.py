from sok.graph.explorer.api.model.graph import Graph

class DataSourcePluginXml(DataLoaderBase):
    def identifier(self):
        return "DataSourcePluginXml"

    def name(self):
        return "Data Source Plugin XML"