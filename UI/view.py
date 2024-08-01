import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None

        self._ddMese = None
        self._ddLuogo = None
        self._txtSPeso = None
        self._btnGraph = None
        self._txtResult1 = None
        self._btnTempo = None
        self._btnStaz = None
        self._btnErr = None
        self._btnMag = None
        self._txtMag = None
        self._txtClass = None
        self._txtResult2 = None
        self._txtSRicorsione = None
        self._btnDensita = None
        self._txtResult3 = None

    def load_interface(self):
        # title
        self._title = ft.Text("Analisi terremoti", color="blue", size=24)
        self._page.controls.append(self._title)

        # Righe 1-2-3 in un Container
        self._ddMese = ft.Dropdown(label="Mese")
        self._ddLuogo = ft.Dropdown(label="Luogo")
        self._txtSPeso = ft.TextField(label="Soglia peso")
        row1 = ft.Row([self._ddMese, self._ddLuogo, self._txtSPeso], alignment=ft.MainAxisAlignment.CENTER)

        self._btnGraph = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handle_graph)
        row2 = ft.Row([self._btnGraph], alignment=ft.MainAxisAlignment.CENTER)

        self._txtResult1 = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        row3 = ft.Row([self._txtResult1], alignment=ft.MainAxisAlignment.CENTER)

        container1 = ft.Container(content=ft.Column([row1, row2, row3], spacing=10))
        self._page.controls.append(container1)

        # Righe 4-5-6 in un altro Container
        self._btnTempo = ft.ElevatedButton("Analisi Temporale", on_click=self._controller.handle_tempo)
        self._btnStaz = ft.ElevatedButton("Analisi Stazioni", on_click=self._controller.handle_stazioni)
        self._btnErr = ft.ElevatedButton("Analisi Errori", on_click=self._controller.handle_errori)
        row4 = ft.Row([self._btnTempo, self._btnStaz, self._btnErr], alignment=ft.MainAxisAlignment.CENTER)

        self._btnMag = ft.ElevatedButton("Analisi Magnitudo", on_click=self._controller.handle_mag)
        self._txtMag = ft.TextField(label="Magnitudo", width=150)
        self._txtClass = ft.TextField(label="Quantità", width=150)
        row5 = ft.Row([self._btnMag, self._txtMag, self._txtClass], alignment=ft.MainAxisAlignment.CENTER)

        self._txtResult2 = ft.ListView(expand=0, spacing=5, padding=5, auto_scroll=True)
        row6 = ft.Row([self._txtResult2], alignment=ft.MainAxisAlignment.CENTER)

        container2 = ft.Container(content=ft.Column([row4, row5, row6], spacing=10))
        self._page.controls.append(container2)

        # Righe 7-8 in un altro Container
        self._txtSRicorsione = ft.TextField(label="Soglia Ricorsione")
        self._btnDensita = ft.ElevatedButton("Analisi Densità", on_click=self._controller.handle_densita)
        row7 = ft.Row([self._txtSRicorsione, self._btnDensita], alignment=ft.MainAxisAlignment.CENTER)

        self._txtResult3 = ft.ListView(expand=0, spacing=5, padding=5, auto_scroll=True)
        row8 = ft.Row([self._txtResult3], alignment=ft.MainAxisAlignment.CENTER)

        container3 = ft.Container(content=ft.Column([row7, row8], spacing=10))
        self._page.controls.append(container3)

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
