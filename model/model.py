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
            self._terremoti = DAO.getTerremoti(mese)
        else:
            self._terremoti = DAO.getTerremotiZona(zona,mese)

        self._grafo.add_nodes_from(self._terremoti)
        print(len(self._grafo.nodes))
        nodi = list(self._grafo.nodes)
        num_nodi = len(nodi)

        for i in range(num_nodi):
            n1 = nodi[i]
            for j in range(i + 1, num_nodi):
                n2 = nodi[j]
                km = geodesic((n1.latitude, n1.longitude), (n2.latitude, n2.longitude)).kilometers
                if km <= soglia:
                    self._grafo.add_edge(n1, n2, weight=km)

    def analisiTemporale(self,mese,diz):
        if len(self._grafo.nodes) == 0:
            return 0,0
        if diz == {}:
            return self.analisiZonaSingola(mese)
        else:
            return self.analisiZone(diz,mese)

    def analisiZonaSingola(self,mese):
        giorni = self.contaGiorni(mese)
        self._terremotiTemp = []
        for t in self._grafo.nodes:
            self._terremotiTemp.append((datetime.strptime(t.time, "%Y-%m-%dT%H:%M:%S.%fZ")).day)
        self._terremotiTemp = sorted(self._terremotiTemp)
        differenze = [self._terremotiTemp[i] - self._terremotiTemp[i - 1] for i in range(1, len(self._terremotiTemp))]
        media_differenze = sum(differenze) / len(differenze)
        return media_differenze, giorni * 24 / len(differenze)

    def analisiZone(self,diz,mese):
        pass
        # for key in diz
        # aggiungere se place assente dal database


    def analisiStazioni(self):
        self._terremotiStaz = []
        for t in self._grafo.nodes:
            if t.nst is not None:
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
            if n.place is not None:
                if n.mag <= (sm+0.5) and n.mag >= (sm-0.5):
                    self._terremotiMag.append((n.place, n.mag))
        return self._terremotiMag

    def trovaClassifica(self):
        self._terremotiClassifica = []
        for n in self._grafo.nodes:
            if n.place is not None:
                self._terremotiClassifica.append((n.place,n.mag))
        self._terremotiClassifica.sort(key=lambda x: x[1], reverse=True)
        return self._terremotiClassifica

    def trovaDensita(self,sr):
        risultati = {}
        for nodo_sorgente in self._grafo.nodes:
            self._sol = set()
            parziale = set()
            self.ricorsione(nodo_sorgente, sr, parziale)
            risultati[nodo_sorgente.place] = len(self._sol)
        return dict(sorted(risultati.items(), key=lambda item: item[1], reverse=True))

    def ricorsione(self, nodo_sorgente, soglia_ricorsione, parziale):
        for nodo in self._grafo.nodes:
            if nodo not in parziale:
                distanza = geodesic((nodo_sorgente.latitude, nodo_sorgente.longitude), (nodo.latitude, nodo.longitude)).kilometers
                if distanza <= soglia_ricorsione:
                    parziale.add(nodo)
                    self.ricorsione(nodo, soglia_ricorsione, parziale)
        self._sol = copy.deepcopy(parziale)

    def stampaGrafo(self):
        return (len(self._grafo.nodes()), len(self._grafo.edges()))

    def contaGiorni(self, mese):
        if mese =="Novembre" or mese =="Aprile" or mese == "Giugno" or mese == "Settembre":
            return 30
        if mese =="Febbbraio":
            return 28
        else:
            return 31

    def clearGraph(self):
        self._grafo.clear()
