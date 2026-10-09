import ttkbootstrap as ttk
from Views.dashboardView import Dashboard
from Views.studentView import Student_Verwalten
from Views.studiengangView import Studiengang_Verwalten


class App(ttk.Window):
    """Stellt das Hauptfenster mit Titel, Größe und Theme bereit."""
    def __init__(self, title: str, size: tuple[int, int], theme='sandstone-light'):
        """Initialisiert das Hauptfenster"""
        super().__init__(title=title, themename=theme)
        self.geometry(f"{size[0]}x{size[1]}")
        print(ttk.Style().theme_names())

class MainWindow(ttk.Frame):
    """Zeigt die Startseite mit Navigation zu den drei Anwendungsbereichen."""
    def __init__(self, parent, controller):
        """Initialisiert das Fenster und verbindet den Controller"""
        super().__init__(parent)
        self.controller = controller
        self._widgets_erstellen()
        self._layout_erstellen()

    def _widgets_erstellen(self):
        """Erstellt Widgets für die Startseite."""
        self.label_title = ttk.Label(self, text="Dashboard Startseite", font=("Arial", 24, 'bold'))
        self.button_studiengang = ttk.Button(
            self,
            text="Studiengänge verwalten",
            bootstyle='primary-outline',
            command=lambda: self.controller.zeige_seite(Studiengang_Verwalten, self.controller)
        )
        self.button_studenten = ttk.Button(
            self,
            text="Studenten verwalten",
            bootstyle='primary-outline',
            command=lambda: self.controller.zeige_seite(Student_Verwalten, self.controller)
        )
        self.button_dashboard = ttk.Button(
            self,
            text="Zum Dashboard",
            bootstyle='primary-outline',
            command=lambda: self.controller.zeige_seite(Dashboard, self.controller)
        )

    def _layout_erstellen(self):
        """Erstellt Layout für die Startseite."""
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure((1, 2, 3, 4, 5, 6, 7), weight=2, uniform='a')

        self.label_title.grid(column=0, row=0, columnspan=3, padx=10, sticky='we')
        self.button_studiengang.grid(column=0, columnspan=2, row=2, rowspan=2, padx=50, pady=10, sticky="nswe")
        self.button_studenten.grid(column=2, columnspan=2, rowspan=2, row=2, padx=50, pady=10, sticky="nswe")
        self.button_dashboard.grid(column=1, columnspan=2, row=5, rowspan=2, padx=50, pady=10, sticky="nswe")