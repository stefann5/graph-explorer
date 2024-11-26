from abc import ABC, abstractmethod
from typing import List

from ..model.graph import Graph


class ServiceBase(ABC):
    @abstractmethod
    def identifier(self):
        pass

    @abstractmethod
    def name(self):
        pass


class DataLoaderBase(ServiceBase):
    @abstractmethod
    def load_graph(self) -> Graph:
        pass


class DataVisualizerBase(ServiceBase):
    @abstractmethod
    def visualize_graph(self, graph:Graph):
        pass