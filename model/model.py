import networkx as nx
from database.dao import DAO
import copy
class Model:
    def __init__(self):
        self.G = nx.DiGraph()

        self.nodes = dict()     #{idartist-int --> obj-artist}
        self.edges = dict()         #{(idartist1-int, idartist2-int) --> peso-float}

        self.ruolo = ""

    def creagrafo(self): # aggiorna self.nodes, self.edges, self.G

        self.G.clear()
        self.nodes.clear()
        self.edges.clear()

        self.nodes= DAO.getnodes(self.ruolo)        #{idartist-int --> obj-artist}
        self.G.add_nodes_from(self.nodes.values())

        self.edges= DAO.getedges(self.ruolo)      #{(idartist1-int, idartist2-int) --> peso-float}
        archi = copy.deepcopy(self.edges)


        for arco in self.edges:
            art1= self.nodes[arco[0]]
            art2= self.nodes[arco[1]]
            peso = abs(art1.indice - art2.indice)
            if art1.indice < art2.indice:
                self.G.add_edge(art1, art2, weight=peso)
                archi[(art1.id, art2.id)] = peso
                if (art2.id, art1.id) in archi:
                    archi.pop((art2.id, art1.id))
            if art1.indice > art2.indice:
                self.G.add_edge(art2, art1, weight=peso)
                archi[(art2.id, art1.id)] = peso
                if (art1.id, art2.id) in archi:
                    archi.pop((art1.id, art2.id))
            if art1.indice == art2.indice:
                archi.pop((art1.id, art2.id))

        self.edges= archi
        pass



        for arco in self.edges.keys():
            art1= self.nodes[arco[0]]
            art2= self.nodes[arco[1]]
            peso =self.edges[arco]
            self.G.add_edge(art1, art2, weight=peso)


    def getnodescollegati(self):
        collegati = set()
        for arco in self.edges:
            collegati.add(arco[0])
            collegati.add(arco[1])
        return len(collegati)




    def get_classifica_influenza(self):  # [(obj-artista, delta-float)]  gia ord
        lista= []
        for n in self.G.nodes():
            pesouscenti= 0
            pesoentranti = 0
            for e_out in self.G.out_edges(n, data=True):
                peso1 = e_out[2]["weight"]
                pesouscenti += peso1
            for e_in in self.G.in_edges(n, data=True):
                peso2 = e_in[2]["weight"]
                pesoentranti += peso2
            pesotot= pesouscenti-pesoentranti
            lista.append((n, pesotot))
        listaord= sorted(lista, key = lambda x: x[1], reverse= True)
        return listaord




    def getruoli(self):      #[ruolo-str]
        ruoli= DAO.getruoli()   #[ruolo-str]
        return ruoli