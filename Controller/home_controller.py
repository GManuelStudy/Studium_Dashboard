from Views.mainWindow import MainWindow, App

class HomeController:
    def __init__(self, app: App, studiengang_controller, student_controller, dashboard_controller) -> None:
        self.app = app
        self.studiengang_controller = studiengang_controller
        self.student_controller = student_controller
        self.dashboard_controller = dashboard_controller
        self.current_page = None
        self.zeige_startseite()

    def zeige_startseite(self):
        self.zeige_seite(MainWindow, self)

    def zeige_seite(self, page, controller, **kwargs):
        if self.current_page is not None:
            for child in self.app.winfo_children():
                child.destroy()

        self.current_page = page(self.app, controller, **kwargs)
        self.current_page.pack(fill="both", expand=True)