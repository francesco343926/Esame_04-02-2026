import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.artists = []

    def build_graph(self, role: str):
        pass

    def classifica(self):
        pass
