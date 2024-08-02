import copy
from datetime import datetime

import networkx as nx
from database.DAO import DAO
from geopy.distance import geodesic


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        pass

    def creaGrafo(self,zona,mese,soglia):
        self._grafo.clear()
        if zona is None or zona.strip() == "":
            self._terremoti = DAO.getTerremoti(mese) #inutilizzabile
        else:
            self._terremoti = DAO.getTerremotiZona(zona,mese)

        self._grafo.add_nodes_from(self._terremoti)
        print(len(self._grafo.nodes))
        for n1 in self._grafo.nodes:
            for n2 in self._grafo.nodes:
                if n1.id > n2.id:
                    km = self.calcolaDistanza(n1,n2)
                    if km <= soglia:
                        self._grafo.add_edge(n1,n2,weight=km)

    def analisiTemporale(self,mese):
        if len(self._grafo.nodes) == 0:
            return 0,0 #torno lista vuota cosi uso il metodo di tutti gli altri

        giorni = self.contaGiorni(mese)
        self._terremotiTemp = []
        for t in self._grafo.nodes:
            self._terremotiTemp.append((datetime.strptime(t.time, "%Y-%m-%dT%H:%M:%S.%fZ")).day)
        self._terremotiTemp = sorted(self._terremotiTemp)
        differenze = [self._terremotiTemp[i] - self._terremotiTemp[i - 1] for i in range(1, len(self._terremotiTemp))]
        media_differenze = sum(differenze) / len(differenze)
        return media_differenze, giorni*24/len(differenze)

    def analisiStazioni(self):
        self._terremotiStaz = []
        for t in self._grafo.nodes:
            if t.nst is None:
                self._terremotiStaz.append((t.place, 0))
            else:
                self._terremotiStaz.append((t.place, t.nst))

        self._terremotiStaz.sort(key=lambda x: x[1])
        return self._terremotiStaz

    def analisiErrori(self):
        self._errh = []
        self._errd = []
        self._errm = []
        for t in self._grafo.nodes:

            if t.horizontalError is None:
                self._errh.append((t.place, 0))
            else:
                self._errh.append((t.place, t.horizontalError))

            if t.depthError is None:
                self._errd.append((t.place, 0))
            else:
                self._errd.append((t.place, t.depthError))

            if t.magError is None:
                self._errm.append((t.place, 0))
            else:
                self._errm.append((t.place, t.magError))

        self._errh.sort(key=lambda x: x[1], reverse=True)
        self._errd.sort(key=lambda x: x[1], reverse=True)
        self._errm.sort(key=lambda x: x[1], reverse=True)

        return self._errh, self._errd, self._errm

    def trovaMagnitudo(self,sm):
        self._terremotiMag = []
        for n in self._grafo.nodes:
            if n.mag <= (sm+0.5) and n.mag >= (sm-0.5):
                self._terremotiMag.append((n.place, n.mag))
        return self._terremotiMag

    def trovaClassifica(self):
        self._terremotiClassifica = []
        for n in self._grafo.nodes:
            self._terremotiClassifica.append((n.place,n.mag))
        self._terremotiClassifica.sort(key=lambda x: x[1], reverse=True)
        return self._terremotiClassifica

    def stampaGrafo(self):
        return (len(self._grafo.nodes()), len(self._grafo.edges()))

    def calcolaDistanza(self, n1, n2):
        punto1 = (n1.latitude, n1.longitude)
        punto2 = (n2.latitude, n2.longitude)
        return geodesic(punto1, punto2).kilometers

    def contaGiorni(self, mese):
        if mese =="Novembre" or mese =="Aprile" or mese == "Giugno" or mese == "Settembre":
            return 30
        if mese =="Febbbraio":
            return 28
        else:
            return 31
