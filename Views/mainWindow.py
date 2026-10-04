import tkinter as tk
import ttkbootstrap as ttk

from Views.dashboardView import Dashboard
from Views.studentView import Student_Verwalten
from Views.studiengangView import Studiengang_Verwalten

from Controller.studiengang_controller import StudiengangController
from Controller.student_controller import StudentController

class App(ttk.Window):
    def __init__(self, title:str, size:tuple[int,int], theme='sandstone-light'):
        super().__init__(title=title, themename=theme)
        self.geometry(f"{size[0]}x{size[1]}")
        print(ttk.Style().theme_names())

class MainWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # self.place(relx=0.5, rely=0.30, anchor="center", relwidth=0.7, relheight=0.8)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.label_title = ttk.Label(self, text="Dashboard Startseite", font=("Arial", 24, 'bold'))
        self.button_studiengang = ttk.Button(self,
                                             text="Studiengänge verwalten",
                                             bootstyle='primary-outline', command= lambda: self.controller.zeige_seite(Studiengang_Verwalten, self.controller))
        self.button_studenten = ttk.Button(self, text="Studenten verwalten", bootstyle='primary-outline', command= lambda: self.controller.zeige_seite(Student_Verwalten, self.controller))
        self.button_dashboard = ttk.Button(self, text="Zum Dashboard", bootstyle='primary-outline', command= lambda: self.controller.zeige_seite(Dashboard, self.controller))

    def create_layout(self):
        self.columnconfigure((0,1,2,3), weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure((1,2,3,4,5,6,7), weight=2, uniform='a')

        self.label_title.grid(column=0, row=0, columnspan=3, padx=10, sticky='we')
        self.button_studiengang.grid(column=0, columnspan=2, row=2, rowspan=2, padx=50, pady=10, sticky="nswe")
        self.button_studenten.grid(column=2, columnspan=2, rowspan=2, row=2, padx=50, pady=10, sticky="nswe")
        self.button_dashboard.grid(column=1, columnspan=2, row=5, rowspan=2, padx=50, pady=10, sticky="nswe")