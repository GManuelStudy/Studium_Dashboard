import ttkbootstrap as ttk

from Model.modul import Modul


class Studiengang_Verwalten(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        # self.place(relx=0.5, rely=0.30, anchor="center", relwidth=0.7, relheight=0.8)
        self.create_widgets()
        self.create_layout()
        self.fill_treeview()

    def create_widgets(self):
        self.label_title = ttk.Label(self.parent, text="Studiengänge verwalten", font=("Arial", 24, 'bold'))

        self.treeview_studiengaenge = ttk.Treeview(self, columns=('row', 'bezeichnung', 'ects_ges', 'anzahl_sem', 'anzahl_mod'), show='headings')
        self.treeview_studiengaenge.heading('row', text='Nr.', anchor='w')
        self.treeview_studiengaenge.heading('bezeichnung', text='Studiengang', anchor='w')
        self.treeview_studiengaenge.heading('ects_ges', text='ECTS Gesamt', anchor='w')
        self.treeview_studiengaenge.heading('anzahl_sem', text='Anzahl Semester', anchor='w')
        self.treeview_studiengaenge.heading('anzahl_mod', text='Anzahl Module', anchor='w')

        self.treeview_studiengaenge.column('row', anchor='w', width=50)
        self.treeview_studiengaenge.column('bezeichnung', anchor='w')
        self.treeview_studiengaenge.column('ects_ges', anchor='w')
        self.treeview_studiengaenge.column('anzahl_sem', anchor='w')
        self.treeview_studiengaenge.column('anzahl_mod', anchor='w')

        self.treeview_studiengaenge.bind('<Delete>', lambda e: self.del_row())
        self.treeview_studiengaenge.bind('<Double-Button-1>', lambda e: self.open_edit())

        self.style = ttk.Style()
        self.style.configure(
            "success.TButton",  # eigener Name
            font=("Helvetica", 18)
        )
        self.button_neu = ttk.Button(self, text='+', bootstyle='success', style='success.TButton', command= lambda: self.controller.zeige_seite(StudiengangForm, self.controller))

        self.frame_buttons = ttk.Frame(self)
        self.button_bearbeiten = ttk.Button(self.frame_buttons, text="Datensatz bearbeiten", bootstyle='primary', command= self.open_edit)
        self.button_loeschen = ttk.Button(self.frame_buttons, text="Datensatz löschen", bootstyle='danger', command= lambda: self.del_row())
        self.button_zurueck = ttk.Button(self.frame_buttons, text="Zurück", bootstyle='secondary', command= lambda: self.controller.zeige_startseite())

    def create_layout(self):
        self.columnconfigure((0,1,2), weight=1, uniform='a')
        self.rowconfigure((0,1,2,3), weight=1, uniform='a')

        self.label_title.pack(side='top', pady=10, padx=10, fill='x', anchor='center')
        self.treeview_studiengaenge.pack(side='top', pady=10, padx=10, fill='both', expand=True)
        self.button_neu.pack(side='top', pady=10, padx=10, anchor='center')
        self.frame_buttons.pack(side='top', pady=10, padx=10, fill='x', anchor='center')
        self.button_bearbeiten.pack(side='right', pady=10, padx=10, anchor='e')
        self.button_loeschen.pack(side='right', pady=10, padx=10, anchor='e')
        self.button_zurueck.pack(side='left', pady=10, padx=10, anchor='w')

    def fill_treeview(self):
        for item in self.treeview_studiengaenge.get_children():
            self.treeview_studiengaenge.delete(item)

        studiengaenge = self.controller.studiengang_controller.get_studiengaenge()
        for nummer, studiengang in enumerate(studiengaenge, 1):
            self.treeview_studiengaenge.insert('', 'end', iid=str(studiengang.studiengang), values=(nummer, studiengang.studiengang, studiengang.ectsGesamt, studiengang.anzahlSemester, studiengang.anzahlModule))

    def del_row(self):
        selection = self.treeview_studiengaenge.selection()
        if not selection:
            return

        for item in selection:
            self.controller.studiengang_controller.del_studiengang(item)

        self.fill_treeview()


    def open_edit(self):
        studiengang = self.controller.studiengang_controller.get_studiengang(self.treeview_studiengaenge.selection()[0])
        self.controller.zeige_seite(StudiengangForm, self.controller, studiengang=studiengang)

class StudiengangForm(ttk.Frame):
    def __init__(self, parent, controller, studiengang=None):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.studiengang = studiengang
        self.edit = studiengang is not None

        self.create_widgets()
        self.create_layout()
        self.fill_treeview()

        if self.edit:
            self.fill_form()

    def create_widgets(self):
        title = "Studiengang bearbeiten" if self.edit else "Studiengang anlegen"
        self.label_title = ttk.Label(self, text=title, font=("Arial", 24, "bold"))

        self.frame_studiengang_form = ttk.Frame(self)
        self.label_studiengang = ttk.Label(self.frame_studiengang_form, text="Studiengang:")
        self.entry_studiengang = ttk.Entry(self.frame_studiengang_form)

        self.button_zurueck = ttk.Button(self, text="Zurück", bootstyle="secondary", command=lambda: self.controller.zeige_seite(Studiengang_Verwalten, self.controller))
        self.button_speichern = ttk.Button(self.frame_studiengang_form, text="Speichern", bootstyle="primary", command=lambda: self.save())

        self.label_modul = ttk.Label(self, text="Module:", font=("Arial", 16, "bold"))

        self.treeview_module = ttk.Treeview(self, columns=('row', 'bezeichnung', 'modul_code', 'ects', 'semester'), show='headings')
        self.treeview_module.heading('row', text='Nr.', anchor='w')
        self.treeview_module.heading('bezeichnung', text='Modulname', anchor='w')
        self.treeview_module.heading('modul_code', text='Modulcode', anchor='w')
        self.treeview_module.heading('ects', text='ECTS', anchor='w')
        self.treeview_module.heading('semester', text='Semester', anchor='w')

        self.treeview_module.column('row', anchor='w', width=50)
        self.treeview_module.column('bezeichnung', anchor='w')
        self.treeview_module.column('modul_code', anchor='w')
        self.treeview_module.column('ects', anchor='w')
        self.treeview_module.column('semester', anchor='w')

        self.treeview_module.bind('<Delete>', lambda e: self.del_row())

        self.button_del_modul = ttk.Button(self, text='Modul löschen', bootstyle='danger', command= lambda: self.del_row())

        self.frame_modul_form = ttk.Frame(self)
        self.label_modulname = ttk.Label(self.frame_modul_form, text="Modulname:")
        self.entry_modulname = ttk.Entry(self.frame_modul_form)
        self.label_modulcode = ttk.Label(self.frame_modul_form, text="Modulcode:")
        self.entry_modulcode = ttk.Entry(self.frame_modul_form)
        self.label_ects = ttk.Label(self.frame_modul_form, text="ECTS:")
        self.entry_ects = ttk.Entry(self.frame_modul_form)
        self.label_semester = ttk.Label(self.frame_modul_form, text="Semester:")
        self.entry_semester = ttk.Entry(self.frame_modul_form)
        self.button_add_modul = ttk.Button(self.frame_modul_form, text="Hinzufügen", bootstyle="primary", command= lambda: self.modul_speichern())

    def create_layout(self):
        self.label_title.pack(side='top', pady=10, padx=10, fill='x', anchor='center')
        self.frame_studiengang_form.pack(side='top', pady=10, padx=10, fill='both', anchor='center')
        self.label_studiengang.pack(side='left', pady=5, padx=10, anchor="w")
        self.entry_studiengang.pack(side='left', pady=5, padx=3, fill="x")
        self.button_speichern.pack(side='left', pady=5)
        self.label_modul.pack(side='top', pady=10, padx=10, anchor="w", fill="x")
        self.treeview_module.pack(side='top', pady=5, padx=10, fill='both', expand=True)

        self.button_del_modul.pack(side='top', pady=5, padx=10, anchor="e")
        self.frame_modul_form.pack(side='top', pady=10, padx=10, fill='x')
        self.frame_modul_form.columnconfigure((0,1,2,3,4), weight=1, uniform='a')
        self.frame_modul_form.rowconfigure((0,1), weight=1, uniform='a')
        self.label_modulname.grid(row=0, column=0, pady=5, padx=10, sticky='we')
        self.entry_modulname.grid(row = 1, column = 0, padx=10, sticky='we')
        self.label_modulcode.grid(row=0, column=1, pady=5, padx=10, sticky='we')
        self.entry_modulcode.grid(row = 1, column = 1, padx=10, sticky='we')
        self.label_ects.grid(row=0, column=2, pady=5, padx=10, sticky='we')
        self.entry_ects.grid(row=1, column=2, padx=10, sticky='we')
        self.label_semester.grid(row=0, column=3, pady=5, padx=10, sticky='we')
        self.entry_semester.grid( row=1, column=3, padx=10, sticky='we')
        self.button_add_modul.grid(row=1, column=4, padx=10, sticky='we')
        self.button_zurueck.pack(side='top', pady=20, padx=20, anchor="w")

    def fill_treeview(self):
        for item in self.treeview_module.get_children():
            self.treeview_module.delete(item)
        if not self.studiengang:
            return
        module = self.controller.studiengang_controller.get_module(self.studiengang)
        for nummer, modul in enumerate(module,1):
            self.treeview_module.insert('', 'end', iid=str(modul.modulcode), values=(nummer, modul.modulname, modul.modulcode, modul.ects, modul.semester.semester))

    def fill_form(self):
        self.entry_studiengang.insert(0, self.studiengang.studiengang)
        # TODO fill treeview_module

    def del_row(self):
        selection = self.treeview_module.selection()
        if not selection:
            return

        for item in selection:
            self.controller.studiengang_controller.del_modul(item)

        self.fill_treeview()

    def modul_speichern(self):
        modulcode = self.entry_modulcode.get().strip()
        modulname = self.entry_modulname.get().strip()
        ects = self.entry_ects.get().strip()
        semester = self.entry_semester.get().strip()
        self.controller.studiengang_controller.add_module(modulname, modulcode, ects, semester, self.studiengang)
        self.fill_treeview()

    def save(self):
        bezeichnung = self.entry_studiengang.get().strip()

        if not bezeichnung:
            return

        if self.edit:
            self.controller.studiengang_controller.update_studiengang(self.studiengang, bezeichnung)
        else:
            studiengang = self.controller.studiengang_controller.add_studiengang(bezeichnung)
            if studiengang is None:
                # studiengang existiert bereits
                return
            self.studiengang = studiengang
            self.edit = True

        self.controller.zeige_seite(Studiengang_Verwalten, self.controller)

    # TODO <delete> binding
    # TODO buttons disablen