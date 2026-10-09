from Views.mainWindow import MainWindow, App

class HomeController:
    """Verwaltet die Navigation zwischen den verschiedenen Fenstern."""
    def __init__(
            self,
            app: App,
            studiengang_controller,
            student_controller,
            dashboard_controller
    ) -> None:
        """Initialisiert HomeController und verbindet Controller"""
        self.app = app
        self.studiengang_controller = studiengang_controller
        self.student_controller = student_controller
        self.dashboard_controller = dashboard_controller
        self.current_page = None
        self.zeige_startseite()

    def zeige_startseite(self) -> None:
        """Navigiert zur Startseite"""
        self.zeige_seite(MainWindow, self)

    def zeige_seite(self, page, controller, **kwargs) -> None:
        """Navigiert zur angegebenen Seite
        page erhält die Klasse des Fensters, controller den jeweiligen Controller.
        kwargs ermöglicht die Übergabe zusätzlicher Parameter wie z.B. Domain-Klassen.
        """
        if self.current_page is not None:
            for child in self.app.winfo_children():
                child.destroy()

        self.current_page = page(self.app, controller, **kwargs)
        self.current_page.pack(fill="both", expand=True)