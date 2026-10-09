from tkinter import messagebox
import ttkbootstrap as ttk
from Views.validierung import (
    studiengang_validieren,
    ects_validieren,
    semester_validieren,
    modulcode_validieren, modulname_validieren
)

class Studiengang_Verwalten(ttk.Frame):
    """Anzeige einer Tabelle und ermöglicht Erstellen, Bearbeiten und Löschen der Studiengänge."""
    def __init__(self, parent, controller):
        """Initialisiert das Studiengang_Verwalten-Fenster und verbindet es mit dem Controller."""
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        # self.place(relx=0.5, rely=0.30, anchor="center", relwidth=0.7, relheight=0.8)
        self._widgets_erstellen()
        self._layout_erstellen()
        self._treeview_befuellen()

    def _widgets_erstellen(self):
        """Erstellt Widgets der Seite und bindet Ereignisse."""
        self.label_title = ttk.Label(
            self.parent, text="Studiengänge verwalten", font=("Arial", 24, 'bold')
        )
        self.treeview_studiengaenge = ttk.Treeview(
            self,
            columns=('row', 'bezeichnung', 'ects_ges', 'anzahl_sem', 'anzahl_mod'),
            show='headings'
        )
        #treeview header
        self.treeview_studiengaenge.heading('row', text='Nr.', anchor='w')
        self.treeview_studiengaenge.heading('bezeichnung', text='Studiengang', anchor='w')
        self.treeview_studiengaenge.heading('ects_ges', text='ECTS Gesamt', anchor='w')
        self.treeview_studiengaenge.heading('anzahl_sem', text='Anzahl Semester', anchor='w')
        self.treeview_studiengaenge.heading('anzahl_mod', text='Anzahl Module', anchor='w')

        # treeview columns
        self.treeview_studiengaenge.column('row', anchor='w', width=50)
        self.treeview_studiengaenge.column('bezeichnung', anchor='w')
        self.treeview_studiengaenge.column('ects_ges', anchor='w')
        self.treeview_studiengaenge.column('anzahl_sem', anchor='w')
        self.treeview_studiengaenge.column('anzahl_mod', anchor='w')

        # treeview aktionen
        self.treeview_studiengaenge.bind('<Delete>', lambda e: self._treeview_zeile_loeschen())
        self.treeview_studiengaenge.bind('<Double-Button-1>', lambda e: self._oeffne_editierungsmodus())
        self.treeview_studiengaenge.bind('<<TreeviewSelect>>', self._treeview_auswahl)

        # style für button_neu
        self.style = ttk.Style()
        self.style.configure(
            "success.TButton",  # eigener Name
            font=("Helvetica", 18)
        )
        self.button_neu = ttk.Button(
            self,
            text='+',
            bootstyle='success',
            style='success.TButton',
            command=lambda: self.controller.zeige_seite(StudiengangForm, self.controller)
        )
        self.frame_buttons = ttk.Frame(self)
        self.button_bearbeiten = ttk.Button(
            self.frame_buttons,
            text="Datensatz bearbeiten",
            bootstyle='primary',
            state='disabled',
            command=self._oeffne_editierungsmodus
        )
        self.button_loeschen = ttk.Button(
            self.frame_buttons,
            text="Datensatz löschen",
            bootstyle='danger',
            state='disabled',
            command=lambda: self._treeview_zeile_loeschen()
        )
        self.button_zurueck = ttk.Button(
            self.frame_buttons,
            text="Zurück",
            bootstyle='secondary',
            command=lambda: self.controller.zeige_startseite()
        )

    def _layout_erstellen(self):
        """Erstellt das Layout der Seite."""
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')

        self.label_title.pack(side='top', pady=10, padx=10, fill='x', anchor='center')
        self.treeview_studiengaenge.pack(side='top', pady=10, padx=10, fill='both', expand=True)
        self.button_neu.pack(side='top', pady=10, padx=10, anchor='center')
        self.frame_buttons.pack(side='top', pady=10, padx=10, fill='x', anchor='center')
        self.button_bearbeiten.pack(side='right', pady=10, padx=10, anchor='e')
        self.button_loeschen.pack(side='right', pady=10, padx=10, anchor='e')
        self.button_zurueck.pack(side='left', pady=10, padx=10, anchor='w')

    def _treeview_befuellen(self):
        """Ersetzt die Tabelleninhalte durch die aktuellen Daten des Controllers."""
        for item in self.treeview_studiengaenge.get_children():
            self.treeview_studiengaenge.delete(item)

        studiengaenge = self.controller.studiengang_controller.lade_alle_studiengaenge()
        for nummer, studiengang in enumerate(studiengaenge, 1):
            self.treeview_studiengaenge.insert(
                '',
                'end',
                iid=str(studiengang.studiengang),
                values=(
                    nummer, studiengang.studiengang, studiengang.ectsGesamt,
                    studiengang.anzahlSemester, studiengang.anzahlModule
                )
            )

    def _treeview_auswahl(self, event=None):
        """Aktiviert oder deaktiviert den Bearbeiten- und Löschen Button bei einer Auswahl."""
        if self.treeview_studiengaenge.selection():
            self.button_loeschen.config(state='normal')
            self.button_bearbeiten.config(state='normal')
        else:
            self.button_loeschen.config(state='disabled')
            self.button_bearbeiten.config(state='disabled')

    def _treeview_zeile_loeschen(self):
        """Löscht ausgewählte Datensätze über den Controller und aktualisiert die Tabelle."""
        selection = self.treeview_studiengaenge.selection()
        if not selection:
            return

        for item in selection:
            studiengang, fehler = self.controller.studiengang_controller.studiengang_loeschen(item)
            if fehler:
                messagebox.showerror("Fehler", fehler)
                return

        self._treeview_befuellen()

    def _oeffne_editierungsmodus(self):
        """Öffnte die StudentenForm mit den ausgewählten Datensatz."""
        if not self.treeview_studiengaenge.selection():
            return
        studiengang, fehler = self.controller.studiengang_controller.lade_studiengang(
            self.treeview_studiengaenge.selection()[0]
        )
        if fehler:
            messagebox.showerror("Fehler", fehler)
            return
        self.controller.zeige_seite(StudiengangForm, self.controller, studiengang=studiengang)

class StudiengangForm(ttk.Frame):
    """Erfasst Studiengänge und verwaltet ihre Module.
    """
    def __init__(self, parent, controller, studiengang=None):
        """Initalisiert die Seite und verbindet sie mit Controller."""
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.studiengang = studiengang
        self.edit = studiengang is not None
        self._widgets_erstellen()
        self._layout_erstellen()
        self._treeview_befuellen()

        # bearbeitungsmodus
        if self.edit:
            self._form_befuellen()

        # buttons und entries aktivieren/deaktivieren
        if self.studiengang is not None:
            self.button_add_modul.config(state='normal')
            self.entry_modulname.config(state='normal')
            self.entry_modulcode.config(state='normal')
            self.entry_ects.config(state='normal')
            self.entry_semester.config(state='normal')
        else:
            self.button_add_modul.config(state='disabled')
            self.entry_modulname.config(state='disabled')
            self.entry_modulcode.config(state='disabled')
            self.entry_ects.config(state='disabled')
            self.entry_semester.config(state='disabled')

    def _widgets_erstellen(self):
        """Erstellt Widgets der Seite und verbindet sie mit ihren Aktionen."""
        title = "Studiengang bearbeiten" if self.edit else "Studiengang anlegen"
        self.label_title = ttk.Label(self, text=title, font=("Arial", 24, "bold"))
        self.frame_studiengang_form = ttk.Frame(self)
        self.label_studiengang = ttk.Label(self.frame_studiengang_form, text="Studiengang:")
        self.entry_studiengang = ttk.Entry(
            self.frame_studiengang_form,
            validate='key',
            validatecommand=(self.register(studiengang_validieren), '%P')
        )
        self.button_zurueck = ttk.Button(
            self,
            text="Zurück",
            bootstyle="secondary",
            command=lambda: self.controller.zeige_seite(Studiengang_Verwalten, self.controller)
        )
        self.button_speichern = ttk.Button(
            self.frame_studiengang_form,
            text="Studiengang speichern",
            bootstyle="primary",
            command=lambda: self.save()
        )
        self.label_modul = ttk.Label(self, text="Module:", font=("Arial", 16, "bold"))
        self.treeview_module = ttk.Treeview(
            self,
            columns=('row', 'bezeichnung', 'modul_code', 'ects', 'semester'),
            show='headings'
        )
        #treeview header
        self.treeview_module.heading('row', text='Nr.', anchor='w')
        self.treeview_module.heading('bezeichnung', text='Modulname', anchor='w')
        self.treeview_module.heading('modul_code', text='Modulcode', anchor='w')
        self.treeview_module.heading('ects', text='ECTS', anchor='w')
        self.treeview_module.heading('semester', text='Semester', anchor='w')
        # treeview columns
        self.treeview_module.column('row', anchor='w', width=50)
        self.treeview_module.column('bezeichnung', anchor='w')
        self.treeview_module.column('modul_code', anchor='w')
        self.treeview_module.column('ects', anchor='w')
        self.treeview_module.column('semester', anchor='w')
        # treeview aktionen
        self.treeview_module.bind('<Delete>', lambda e: self._treeview_zeile_loeschen())
        self.treeview_module.bind('<<TreeviewSelect>>', self._treeview_auswahl)

        self.button_del_modul = ttk.Button(
            self,
            text='Modul löschen',
            bootstyle='danger',
            state='disabled',
            command=lambda: self._treeview_zeile_loeschen()
        )
        # modulformular
        self.frame_modul_form = ttk.Frame(self)
        self.label_modulname = ttk.Label(self.frame_modul_form, text="Modulname:")
        self.entry_modulname = ttk.Entry(
            self.frame_modul_form,
            validate='key',
            validatecommand=(self.register(modulname_validieren), '%P')
        )
        self.label_modulcode = ttk.Label(self.frame_modul_form, text="Modulcode:")
        self.entry_modulcode = ttk.Entry(
            self.frame_modul_form,
            validate='key',
            validatecommand=(self.register(modulcode_validieren), '%P')
        )
        self.label_ects = ttk.Label(self.frame_modul_form, text="ECTS:")
        self.entry_ects = ttk.Entry(
            self.frame_modul_form,
            validate='key',
            validatecommand=(self.register(ects_validieren), '%P')
        )
        self.label_semester = ttk.Label(self.frame_modul_form, text="Semester:")
        self.entry_semester = ttk.Entry(
            self.frame_modul_form,
            validate='key',
            validatecommand=(self.register(semester_validieren), '%P')
        )
        self.button_add_modul = ttk.Button(
            self.frame_modul_form,
            text="Hinzufügen",
            bootstyle="primary",
            state='disabled',
            command=lambda: self.modul_speichern()
        )

    def _layout_erstellen(self):
        """Erstellt das Layout der Seite."""
        # studiengang layout
        self.label_title.pack(side='top', pady=10, padx=10, fill='x', anchor='center')
        self.frame_studiengang_form.pack(side='top', pady=10, padx=10, fill='both', anchor='center')
        self.label_studiengang.pack(side='left', pady=5, padx=10, anchor="w")
        self.entry_studiengang.pack(side='left', pady=5, padx=3, fill="x")
        self.button_speichern.pack(side='left', pady=5)

        # modul layout
        self.label_modul.pack(side='top', pady=10, padx=10, anchor="w", fill="x")
        self.treeview_module.pack(side='top', pady=5, padx=10, fill='both', expand=True)
        self.button_del_modul.pack(side='top', pady=5, padx=10, anchor="e")
        self.frame_modul_form.pack(side='top', pady=10, padx=10, fill='x')
        self.frame_modul_form.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        self.frame_modul_form.rowconfigure((0, 1), weight=1, uniform='a')
        self.label_modulname.grid(row=0, column=0, pady=5, padx=10, sticky='we')
        self.entry_modulname.grid(row=1, column=0, padx=10, sticky='we')
        self.label_modulcode.grid(row=0, column=1, pady=5, padx=10, sticky='we')
        self.entry_modulcode.grid(row=1, column=1, padx=10, sticky='we')
        self.label_ects.grid(row=0, column=2, pady=5, padx=10, sticky='we')
        self.entry_ects.grid(row=1, column=2, padx=10, sticky='we')
        self.label_semester.grid(row=0, column=3, pady=5, padx=10, sticky='we')
        self.entry_semester.grid(row=1, column=3, padx=10, sticky='we')
        self.button_add_modul.grid(row=1, column=4, padx=10, sticky='we')
        self.button_zurueck.pack(side='top', pady=20, padx=20, anchor="w")

    def _treeview_befuellen(self):
        """Befüllt die Treeview mit Modul-Objekten des Controllers."""
        for item in self.treeview_module.get_children():
            self.treeview_module.delete(item)
        if not self.studiengang:
            return
        module, fehler = self.controller.studiengang_controller.lade_module_von_studiengang(self.studiengang)
        if fehler:
            messagebox.showerror("Fehler", fehler)
            self.controller.zeige_seite(Studiengang_Verwalten, self.controller)
            return
        for nummer, modul in enumerate(module, 1):
            self.treeview_module.insert(
                '',
                'end',
                iid=str(modul.modulcode),
                values=(
                    nummer, modul.modulname, modul.modulcode,
                    modul.ects, modul.semester.semester
                )
            )

    def _treeview_auswahl(self, event=None):
        """Aktiviert oder deaktiviert den Bearbeiten- und Löschen Button bei einer Auswahl."""
        if self.treeview_module.selection():
            self.button_del_modul.config(state='normal')
        else:
            self.button_del_modul.config(state='disabled')

    def _form_befuellen(self):
        """Befüllt die Formularfelder mit dem vorhandenen Objekt im Bearbeitungsmodus."""
        self.entry_studiengang.insert(0, self.studiengang.studiengang)

    def _treeview_zeile_loeschen(self):
        """Löscht ausgewählte Datensätze über den Controller und aktualisiert die Tabelle."""
        selection = self.treeview_module.selection()
        if not selection:
            return

        for item in selection:
            self.controller.studiengang_controller.modul_loeschen(item, self.studiengang)

        self._treeview_befuellen()

    def modul_speichern(self):
        """Übergibt Modulfelder an den Controller und aktualisiert die Modultabelle."""
        modulcode = self.entry_modulcode.get().strip()
        modulname = self.entry_modulname.get().strip()
        ects = self.entry_ects.get().strip()
        semester = self.entry_semester.get().strip()
        modul, fehler = self.controller.studiengang_controller.modul_hinzufuegen(
            modulname,
            modulcode,
            ects,
            semester,
            self.studiengang
        )
        if fehler:
            messagebox.showerror("Fehler", fehler)
            return
        self._treeview_befuellen()

    def save(self):
        """Speichert die Studiengangbezeichnung und öffnet das Formular mit dem Ergebnis."""
        bezeichnung = self.entry_studiengang.get().strip()
        if bezeichnung == "":
            messagebox.showerror("Fehler", "Bitte geben Sie einen Studiengang an.")
            return
        if self.edit:
            studiengang, fehler = self.controller.studiengang_controller.studiengang_aktualisieren(
                self.studiengang, bezeichnung
            )
        else:
            studiengang, fehler = self.controller.studiengang_controller.studiengang_hinzufuegen(bezeichnung)
            self.studiengang = studiengang
            self.edit = True
        if fehler:
            messagebox.showerror("Fehler", fehler)
            self.controller.zeige_seite(Studiengang_Verwalten, self.controller)
            return
        self.controller.zeige_seite(StudiengangForm, self.controller, studiengang=self.studiengang)