import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDluoghi(self):
        self._dizionarioAnalisiTemp = {}
        self._luoghi = DAO.getLuoghi()
        for l in self._luoghi:
            self._view._ddLuogo.options.append(ft.dropdown.Option(l))
        pass

    def fillDDMesi(self):
        mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre",
                "Ottobre", "Novembre", "Dicembre"]
        for i in range(len(mesi)):
            self._view._ddMese.options.append(ft.dropdown.Option(mesi[i]))
        pass

    def handle_select(self,e):
        self._view._txtResult1.controls = None
        self._view._txtSPeso.value = ""
        self._view._ddMese.value = None
        self._view._ddLuogo.value = None
        self._model.clearGraph()
        self._view._btnTempo.disabled = True
        self._view._btnStaz.disabled = True
        self._view._btnErr.disabled = True
        self._view._btnMag.disabled = True
        self._view._ddMag.disabled = True
        self._view._btnClass.disabled = True
        self._view._ddClass.disabled = True
        self._view._txtSRicorsione.disabled = True
        self._view._btnDensita.disabled = True
        self._view._ddClass.options = []
        self._view._ddMag.options = []
        self._view.update_page()

    # def handle_choose(self,e):
    #     dizScelta = {}
    #     for z in self._luoghi:
    #         dizScelta[z] = len(DAO.getTerremotiZona(self.convertiZona(z),self.convertiData(self._view._ddMese.value)))
    #     listaFinale = sorted(dizScelta.items(), key=lambda item: item[1])
    #     self._view._txtResult2.controls.append(ft.Text(f"-> Zone consigliate"))
    #
    #     for nodo, conteggio in listaFinale:
    #         self._view._txtResult2.controls.append(ft.Text(f"{nodo} con {conteggio} terremoti"))
    #
    #     self._view._txtResult2.controls.append(ft.Text(f""))
    #     self._view.update_page()

    def handle_graph(self, e):
        if self._view._ddMese.value is None:
            self._view.create_alert("Inserisci un mese per l'analisi")
            return

        mese = self.convertiData(self._view._ddMese.value)

        if self._view._txtSPeso.value is None or self._view._txtSPeso.value.strip() == "":
            soglia = 0
        else:
            try:
                float(self._view._txtSPeso.value)
            except ValueError:
                if ',' in self._view._txtSPeso.value:
                    self._view.create_alert("Il valore decimale richiede il punto")
                    return
                self._view.create_alert("Inserisci un valore numerico per la soglia")
                return
            soglia = self._view._txtSPeso.value

        zona = self.convertiZona(self._view._ddLuogo.value)
        if zona is None:
            self._dizionarioAnalisiTemp = {item: None for item in self._luoghi}
        self._model.creaGrafo(zona, mese, float(soglia))
        n,e = self._model.stampaGrafo()
        if zona is None:
            self._view._txtResult1.controls.append(ft.Text(f"Rilevati {n} terremoti con {e} connessioni nel mondo nel mese di {self._view._ddMese.value}"))

        self._view._txtResult1.controls.append(ft.Text(f"Rilevati {n} terremoti con {e} connessioni nella regione {self._view._ddLuogo.value} nel mese di {self._view._ddMese.value}"))
        self._view._btnTempo.disabled = False
        self._view._btnStaz.disabled = False
        self._view._btnErr.disabled = False
        self._view._btnMag.disabled = False
        self._view._ddMag.disabled = False
        self._view._btnClass.disabled = False
        self._view._ddClass.disabled = False
        self._view._txtSRicorsione.disabled = False
        self._view._btnDensita.disabled = False
        self._view._ddClass.options = []
        self._view._ddMag.options = []

        for i in range(len(self._model._grafo.nodes)):
            if i > 1:
                self._view._ddClass.options.append(ft.dropdown.Option(str(i + 1)))

        self._listmag = [t.mag for t in self._model._grafo.nodes]
        self._listmag = sorted(set(self._listmag))
        for m in self._listmag:
            self._view._ddMag.options.append(ft.dropdown.Option(str(m)))

        self._view.update_page()
        pass

    def handle_tempo(self, e):
        # metti a posto distanza
        distanza, frequenza = self._model.analisiTemporale(self._view._ddMese.value, self._dizionarioAnalisiTemp)
        # distanza puo essere sia un numero che un dizionario in base all'input del Flet
        if frequenza == 0:
            self._view.create_alert(f"Non sono avvenuti terremoti in questo periodo nella zona selezionata")
            return
        self._view._txtResult2.controls.append(ft.Text(f"-> Analisi temporale:"))

        if self._dizionarioAnalisiTemp == {}:
            self._view._txtResult2.controls.append(ft.Text(
                f"Nel mese di {self._view._ddMese.value} nella zona {self._view._ddLuogo.value} si è verificato 1 terremoto ogni {round(distanza, 2)} giorni a distanza media di {round(frequenza, 2)} ore"))

        else:
            pass
            # per ogni chiave di "distanza"
            # visualizzo la frequenza in cui sono avvenuti nel mondo
            # e per ogni zona mostro i dettagli sulla distanza media tra una zona e
            # l'altra self._view._txtResult2.controls.append(
            # ft.Text( f"Nel mese di {self._view._ddMese.value} nella zona {CHIAVE} si è verificato 1 terremoto ogni
            # {round(VALORE, 2)} giorni a distanza media di {round(frequenza, 2)} ore"))

        self._view._txtResult2.controls.append(ft.Text(f""))
        self._view.update_page()
        pass

    def handle_stazioni(self, e):
        lista = self._model.analisiStazioni()
        if len(lista) == 0:
            self._view.create_alert(f"Nessuna stazione ha rilevato terremoti in questo periodo nella zona selezionata")
            return
        self._view._txtResult2.controls.append(ft.Text(f"-> Analisi stazioni installate:"))
        for l in lista:
            self._view._txtResult2.controls.append(ft.Text(f"Terremoto a {l[0]} rilevato da {int(l[1])} stazioni"))
        self._view._txtResult2.controls.append(ft.Text(f""))
        self._view.update_page()
        pass

    def handle_errori(self, e):
        listah, listad, listam = self._model.analisiErrori()
        if len(listah) == 0:
            self._view.create_alert(f"Nessuna stazione ha rilevato terremoti in questo periodo nella zona selezionata")
            return
        self._view._txtResult2.controls.append(ft.Text(f"-> Analisi efficacia stazioni:"))
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

    def handle_mag(self, e):
        if len(self._model._grafo.nodes) == 0:
            self._view.create_alert(f"Non sono avvenuti terremoti in questo periodo nella zona selezionata")
            return

        if self._view._ddMag.value is None:
            self._view.create_alert("Inserisci la magnitudo")
            return

        self._view._txtResult2.controls.append(ft.Text(
            f"-> Ricerca luoghi in cui sono avvenuti terremoti con magnitudo vicina a {self._view._ddMag.value}"))
        lista = self._model.trovaMagnitudo(float(self._view._ddMag.value))
        self._view._txtResult2.controls.append(ft.Text(f"Trovati {len(lista)} terremoti"))
        for l in lista:
            self._view._txtResult2.controls.append(ft.Text(f"Terremoto a {l[0]} con magnitudo: {l[1]}"))

        self._view._txtResult2.controls.append(ft.Text(f""))
        self._view.update_page()
        pass

    def handle_class(self, e):
        if len(self._model._grafo.nodes) == 0:
            self._view.create_alert(f"Non sono avvenuti terremoti in questo periodo nella zona selezionata")
            return

        if self._view._ddClass.value is None:
            self._view.create_alert("Inserisci la lunghezza della classifica")
            return

        lista = self._model.trovaClassifica()

        self._view._txtResult2.controls.append(
            ft.Text(f"-> Classifica dei {self._view._ddClass.value} terremoti più forti"))
        num = int(self._view._ddClass.value)

        for l in lista[:num]:
            self._view._txtResult2.controls.append(ft.Text(f"{l[0]}: {l[1]}"))

        self._view._txtResult2.controls.append(
            ft.Text(f"-> Classifica dei {self._view._ddClass.value} terremoti più deboli"))
        for l in lista[-num:]:
            self._view._txtResult2.controls.append(ft.Text(f"{l[0]}: {l[1]}"))
        self._view._txtResult2.controls.append(ft.Text(f""))
        self._view.update_page()

    def handle_clear(self, e):
        self._view._txtResult2.controls = None
        self._view._txtResult3.controls = None
        self._view.update_page()

    def handle_densita(self, e):
        try:
            float(self._view._txtSRicorsione.value)
        except ValueError:
            if ',' in self._view._txtSRicorsione.value:
                self._view.create_alert("Il valore decimale richiede il punto")
                return
            self._view.create_alert("Inserisci un valore numerico per la soglia")
            return
        sr = float(self._view._txtSRicorsione.value)
        elenco = self._model.trovaDensita(sr)
        self._view._txtResult3.controls.append(ft.Text(f"->Analisi densità nel raggio di {sr} km"))
        for nodo, conteggio in elenco.items():
            if conteggio == 1:
                self._view._txtResult3.controls.append(
                    ft.Text(f"1 terremoto intorno a {nodo} {round((conteggio) / ((sr ** 2) * 3.14), 4)} terremoti/km^2"))
            else:
                self._view._txtResult3.controls.append(
                    ft.Text(f"{conteggio} terremoti intorno a {nodo} {round((conteggio) / ((sr ** 2) * 3.14), 4)} terremoti/km^2"))

        self._view._txtResult3.controls.append(ft.Text(f""))
        self._view.update_page()
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

    def nonPossoAnalizzare(self, lista):
        if len(lista) == 0:
            self._view._txtResult2.controls.append(ft.Text(f"La regione selezionata non ha terremoti da analizzare"))
            self._view.update_page()
            return True
        return False
