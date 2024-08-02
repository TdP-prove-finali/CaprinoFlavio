import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDluoghi(self):
        self._luoghi = DAO.getLuoghi()
        for l in self._luoghi:
            self._view._ddLuogo.options.append(ft.dropdown.Option(l))
        pass

    def fillDDMesi(self):
        mesi = ["Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno","Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre"]
        for i in range(len(mesi)):
            self._view._ddMese.options.append(ft.dropdown.Option(mesi[i]))
        pass

    def handle_graph(self, e):
        if self._view._ddMese.value is None:
            self._view.create_alert("Inserisci un mese per l'analisi")
            return
        mese = self.convertiData(self._view._ddMese.value)

        if self._view._txtSPeso.value is None or self._view._txtSPeso.value.strip() == "":
            soglia = 0
        else:
            soglia = self._view._txtSPeso.value

        zona = self.convertiZona(self._view._ddLuogo.value)
        self._model.creaGrafo(zona,mese,int(soglia))
        self._view._txtResult1.controls.append(ft.Text(f"Grafo creato con nodi e archi {self._model.stampaGrafo()}"))
        self._view._btnTempo.disabled= False
        self._view._btnStaz.disabled= False
        self._view._btnErr.disabled= False
        self._view._btnMag.disabled= False
        self._view._ddMag.disabled= False
        self._view._btnClass.disabled= False
        self._view._ddClass.disabled= False
        self._view._txtSRicorsione.disabled= False
        self._view._btnDensita.disabled= False
        self._view._ddClass.options = []
        self._view._ddMag.options = []
        for i in range(len(self._model._grafo.nodes)):
            if i >1: # una classifica almeno 3
                self._view._ddClass.options.append(ft.dropdown.Option(str(i+1)))


        self._listmag = [t.mag for t in self._model._grafo.nodes]
        self._listmag = sorted(set(self._listmag))
        for m in self._listmag:
            self._view._ddMag.options.append(ft.dropdown.Option(str(m)))
        self._view.update_page()
        pass

    def handle_tempo(self,e):
        self._view._txtResult2.controls.append(ft.Text(f"-> Analisi temporale:"))
        distanza, frequenza = self._model.analisiTemporale(self._view._ddMese.value)
        self._view._txtResult2.controls.append(ft.Text(f"Nel mese di {self._view._ddMese.value} nella zona {self._view._ddLuogo.value} si è verificato 1 terremoto ogni {round(distanza, 2)} giorni a distanza media di {round(frequenza, 2)} ore"))
        self._view._txtResult2.controls.append(ft.Text(f""))
        self._view.update_page()
        pass

    def handle_stazioni(self,e):
        self._view._txtResult2.controls.append(ft.Text(f"-> Analisi stazioni installate:"))
        lista = self._model.analisiStazioni()
        for l in lista:
            self._view._txtResult2.controls.append(ft.Text(f"Terremoto a {l[0]} rilevato da {int(l[1])} stazioni"))
        self._view._txtResult2.controls.append(ft.Text(f""))
        self._view.update_page()
        pass

    def handle_errori(self,e):
        self._view._txtResult2.controls.append(ft.Text(f"-> Analisi efficacia stazioni:"))
        listah, listad, listam = self._model.analisiErrori()

        self._view._txtResult2.controls.append(ft.Text(f"-> Horizontal error:"))
        for l in listah:
            self._view._txtResult2.controls.append(ft.Text(f"Stazioni a {l[0]}, errore: {l[1]}"))
        self._view._txtResult2.controls.append(ft.Text(f"-> Depth error:"))
        for l in listad:
            self._view._txtResult2.controls.append(ft.Text(f"Stazioni a {l[0]}, errore: {l[1]}"))
        self._view._txtResult2.controls.append(ft.Text(f"-> Mag error:"))
        for l in listam:
            self._view._txtResult2.controls.append(ft.Text(f"Stazioni a {l[0]}, errore: {l[1]}"))
        self._view._txtResult2.controls.append(ft.Text(f""))
        self._view.update_page()
        pass

    def handle_mag(self,e):
        if (self._view._ddMag.value is None):
            self._view.create_alert("Inserisci la magnitudo")
            return

        self._view._txtResult2.controls.append(ft.Text(f"-> Ricerca luoghi in cui sono avvenuti terremoti con magnitudo vicina a {self._view._ddMag.value}"))
        lista = self._model.trovaMagnitudo(float(self._view._ddMag.value))
        for l in lista:
            self._view._txtResult2.controls.append(ft.Text(f"Terremoto a {l[0]} con magnitudo: {l[1]}"))

        self._view._txtResult2.controls.append(ft.Text(f""))
        self._view.update_page()
        pass

    def handle_class(self,e):
        if (self._view._ddClass.value is None):
            self._view.create_alert("Inserisci la lunghezza della classifica")
            return

        self._view._txtResult2.controls.append(ft.Text(f"-> Classifica dei {self._view._ddClass.value} terremoti più forti"))
        lista = self._model.trovaClassifica()
        num = int(self._view._ddClass.value)

        for l in lista[:num]:
            self._view._txtResult2.controls.append(ft.Text(f"{l[0]}: {l[1]}"))

        self._view._txtResult2.controls.append(ft.Text(f"-> Classifica dei {self._view._ddClass.value} terremoti più deboli"))
        for l in lista[-num:]:
            self._view._txtResult2.controls.append(ft.Text(f"{l[0]}: {l[1]}"))
        self._view._txtResult2.controls.append(ft.Text(f""))
        self._view.update_page()

    def handle_densita(self,e):
        pass

    def convertiData(self, param):
        if param == "Gennaio":
            return "2023-01%"
        elif param == "Febbraio":
            return "2023-02%"
        elif param == "Marzo":
            return "2023-03%"
        elif param == "Aprile":
            return "2023-04%"
        elif param == "Maggio":
            return "2023-05%"
        elif param == "Giugno":
            return "2023-06%"
        elif param == "Luglio":
            return "2023-07%"
        elif param == "Agosto":
            return "2023-08%"
        elif param == "Settembre":
            return "2023-09%"
        elif param == "Ottobre":
            return "2023-10%"
        elif param == "Novembre":
            return "2023-11%"
        elif param == "Dicembre":
            return "2023-12%"
        pass

    def convertiZona(self, value):
        if value is None:
            return
        return f"%{value}%"
