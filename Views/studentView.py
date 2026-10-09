import ttkbootstrap as ttk
from tkinter import messagebox
import tkinter as tk
from tksheet import Sheet

from Model.modul import Modul
from Views.validierung import (
    vorname_validieren,
    nachname_validieren,
    matrikelnummer_validieren,
    note_validieren,
    zielnotendurchschnitt_validieren
)
from Model.studiengang import Studiengang

class Student_Verwalten(ttk.Frame):
    """Anzeige einer Tabelle und ermöglicht Erstellen, Bearbeiten und Löschen der Studenten."""
    def __init__(self, parent, controller):
        """Initialisierung der Seite und verbindet sie mit Controller."""
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self._widgets_erstellen()
        self._treeview_befuellen()
        self._layout_erstellen()

    def _widgets_erstellen(self):
        """Erstellt Widgets der Seite und verbindet sie mit ihren Aktionen."""
        self.label_title = ttk.Label(self.parent, text="Studenten verwalten", font=("Arial", 24, 'bold'))
        self.treeview_studenten = ttk.Treeview(
            self,
            columns=(
                'row', 'vorname', 'nachname', 'matrikelnummer',
                'studiengang', 'notendurchschnitt_goal', 'beginn', 'ende'
            ),
            show='headings'
        )
        # treeview header
        self.treeview_studenten.heading('row', text='Nr.', anchor='w')
        self.treeview_studenten.heading('vorname', text='Vorname', anchor='w')
        self.treeview_studenten.heading('nachname', text='Nachname', anchor='w')
        self.treeview_studenten.heading('matrikelnummer', text='Matrikelnummer', anchor='w')
        self.treeview_studenten.heading('studiengang', text='Studiengang', anchor='w')
        self.treeview_studenten.heading('notendurchschnitt_goal', text='Zielnotendurchschnitt', anchor='w')
        self.treeview_studenten.heading('beginn', text='Beginndatum', anchor='w')
        self.treeview_studenten.heading('ende', text='Enddatum', anchor='w')

        # treeview columns
        self.treeview_studenten.column('row', anchor='w', width=50)
        self.treeview_studenten.column('vorname', anchor='w', width=120)
        self.treeview_studenten.column('nachname', anchor='w', width=120)
        self.treeview_studenten.column('matrikelnummer', anchor='w', width=120)
        self.treeview_studenten.column('studiengang', anchor='w', width=280)
        self.treeview_studenten.column('notendurchschnitt_goal', anchor='w', width=150)
        self.treeview_studenten.column('beginn', anchor='w', width=120)
        self.treeview_studenten.column('ende', anchor='w')

        # treeview aktionen
        self.treeview_studenten.bind('<Delete>', lambda e: self._treeview_zeile_loeschen())
        self.treeview_studenten.bind('<Double-Button-1>', lambda e: self._oeffne_editierungsmodus())
        self.treeview_studenten.bind('<<TreeviewSelect>>', self._treeview_auswahl)

        # Style für button_neu
        self.style = ttk.Style()
        self.style.configure(
            "success.TButton",
            font=("Helvetica", 18)
        )
        self.button_neu = ttk.Button(
            self,
            text='+',
            bootstyle='success',
            style='success.TButton',
            command=lambda: self.controller.zeige_seite(StudentenForm, self.controller)
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
            command=self._treeview_zeile_loeschen
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
        self.treeview_studenten.pack(side='top', pady=10, padx=10, fill='both', expand=True)
        self.button_neu.pack(side='top', pady=10, padx=10, anchor='center')
        self.frame_buttons.pack(side='top', pady=10, padx=10, fill='x', anchor='center')
        self.button_bearbeiten.pack(side='right', pady=10, padx=10, anchor='e')
        self.button_loeschen.pack(side='right', pady=10, padx=10, anchor='e')
        self.button_zurueck.pack(side='left', pady=10, padx=10, anchor='w')

    def _treeview_befuellen(self):
        """Ersetzt die Tabelleninhalte durch die Daten des Controllers."""
        for item in self.treeview_studenten.get_children():
            self.treeview_studenten.delete(item)

        studenten = self.controller.student_controller.lade_alle_studenten()
        for nummer, student in enumerate(studenten, 1):
            beginn = student.beginndatum.strftime("%d.%m.%Y")
            ende = student.zielabschlussdatum.strftime("%d.%m.%Y")
            self.treeview_studenten.insert(
                '',
                'end',
                iid=str(student.matrikelnummer),
                values=(
                    nummer,
                    student.vorname,
                    student.nachname,
                    student.matrikelnummer,
                    student.studiengang.studiengang,
                    student.zielnotendurchschnitt,
                    beginn,
                    ende
                )
            )

    def _treeview_auswahl(self, event=None):
        """Aktiviert oder deaktiviert den Bearbeiten- und Löschen Button bei einer Auswahl."""
        if self.treeview_studenten.selection():
            self.button_loeschen.config(state='normal')
            self.button_bearbeiten.config(state='normal')
        else:
            self.button_loeschen.config(state='disabled')
            self.button_bearbeiten.config(state='disabled')

    def _treeview_zeile_loeschen(self):
        """Löscht ausgewählte Datensätze über den Controller und aktualisiert die Tabelle."""
        selection = self.treeview_studenten.selection()
        if not selection:
            return

        for item in selection:
            self.controller.student_controller.student_loeschen(item)

        self._treeview_befuellen()

    def _oeffne_editierungsmodus(self):
        """Öffnte die StudentenForm mit den ausgewählten Datensatz."""
        if not self.treeview_studenten.selection():
            return
        student, fehler = self.controller.student_controller.lade_student(self.treeview_studenten.selection()[0])
        if fehler:
            tk.messagebox.showerror("Fehler", fehler)
            self.controller.zeige_seite(Student_Verwalten, self.controller)
        self.controller.zeige_seite(StudentenForm, self.controller, student=student)


class StudentenForm(ttk.Frame):
    """Erfasst Studentenstammdaten und bearbeitet vorhandene Modulnoten.
    student=None öffnet den Anlegemodus, mit Student den Bearbeitungsmodus.
    """
    def __init__(self, parent, controller, student=None):
        """Initalisiert die Seite und verbindet sie mit Controller."""
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.student = student
        self.edit = student is not None
        self.studiengaenge = []
        self._widgets_erstellen()
        self._combobox_befuellen()
        self._layout_erstellen()

        # im Bearbeitungsmodus
        if self.edit:
            self._form_befuellen()
            self._treeview_befuellen()

    def _widgets_erstellen(self):
        """Erstellt Widgets der Seite und verbindet sie mit ihren Aktionen."""
        title = "Studenten bearbeiten" if self.edit else "Studenten anlegen"
        self.label_title = ttk.Label(self, text=title, font=("Arial", 24, "bold"))
        self.frame_studenten_form = ttk.Frame(self)
        self.label_vorname = ttk.Label(self.frame_studenten_form, text="Vorname:")
        self.entry_vorname = ttk.Entry(
            self.frame_studenten_form,
            validate='key',
            validatecommand=(self.register(vorname_validieren), '%P')
        )
        self.label_nachname = ttk.Label(self.frame_studenten_form, text="Nachname:")
        self.entry_nachname = ttk.Entry(
            self.frame_studenten_form,
            validate='key',
            validatecommand=(self.register(nachname_validieren), '%P')
        )
        self.label_matrikelnummer = ttk.Label(self.frame_studenten_form, text="Matrikelnummer:")
        self.entry_matrikelnummer = ttk.Entry(
            self.frame_studenten_form,
            validate='key',
            validatecommand=(self.register(matrikelnummer_validieren), '%P')
        )
        self.label_studiengang = ttk.Label(self.frame_studenten_form, text="Studiengang:")
        self.str_var_studiengang = tk.StringVar()
        self.combobox_studiengang = ttk.Combobox(
            self.frame_studenten_form,
            state='readonly',
            textvariable=self.str_var_studiengang
        )
        self.label_notendurchschnitt_goal = ttk.Label(
            self.frame_studenten_form,
            text="Zielnotendurch-\nschnitt:"
        )
        self.entry_notendurchschnitt_goal = ttk.Entry(
            self.frame_studenten_form,
            validate='key',
            validatecommand=(self.register(zielnotendurchschnitt_validieren), '%P')
        )
        self.label_beginn = ttk.Label(self.frame_studenten_form, text="Beginndatum:")
        self.entry_beginn = ttk.DateEntry(self.frame_studenten_form)
        self.label_ende = ttk.Label(self.frame_studenten_form, text='Enddatum:')
        self.entry_ende = ttk.DateEntry(self.frame_studenten_form)
        self.button_save_student = ttk.Button(
            self.frame_studenten_form,
            text="Student speichern",
            bootstyle="primary",
            command=self._student_speichern
        )

        for date_entry in (self.entry_beginn, self.entry_ende):
            date_entry.entry.bind('<Key>', lambda e: 'break')
            date_entry.entry.bind('<<Paste>>', lambda e: 'break')
            date_entry.entry.bind('<Button-2>', lambda e: 'break')

        self.frame_module = ttk.Frame(self)
        self.label_modul = ttk.Label(self.frame_module, text="Module:", font=("Arial", 16, "bold"))
        self.treeview_module = Sheet(
            self.frame_module,
            headers=['Modulname', 'Modulcode', 'ECTS', 'Semester', 'Erreichte Note'],
            height=200,
            auto_resize_columns=170,
            table_wrap='w'
        )
        self.treeview_module.edit_validation(self._note_pruefen)
        self.treeview_module.enable_bindings('edit_cell', 'single_select')
        # Nur die Note kann bearbeitet werden.
        self.treeview_module.readonly_columns([0, 1, 2, 3])
        self.frame_module.bind('<Configure>', lambda e: self.treeview_module.set_all_row_heights())

        self.button_modul = ttk.Button(
            self.frame_module,
            text="Note Eintragen",
            state='disabled',
            bootstyle="primary",
            command=self._note_eintragen
        )

        self.button_zurueck = ttk.Button(
            self,
            text="Zurück",
            bootstyle='secondary',
            command=lambda: self.controller.zeige_seite(Student_Verwalten, self.controller)
        )

    def _layout_erstellen(self):
        """Erstellt das Layout der Seite."""
        # studenten-Form Layout
        self.label_title.pack(side='top', pady=10, padx=10, fill='x', anchor='center')
        self.frame_studenten_form.pack(side='top', pady=10, padx=10, fill='both', anchor='center')
        self.frame_studenten_form.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform='a')
        self.frame_studenten_form.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.label_vorname.grid(row=0, column=1, pady=5, padx=10, sticky='we')
        self.entry_vorname.grid(row=0, column=2, columnspan=2, padx=10, sticky='we')
        self.label_nachname.grid(row=0, column=4, pady=5, padx=10, sticky='we')
        self.entry_nachname.grid(row=0, column=5, columnspan=2, padx=10, sticky='we')
        self.label_matrikelnummer.grid(row=1, column=1, pady=5, padx=10, sticky='we')
        self.entry_matrikelnummer.grid(row=1, column=2, columnspan=2, padx=10, sticky='we')
        self.label_studiengang.grid(row=1, column=4, pady=5, padx=10, sticky='we')
        self.combobox_studiengang.grid(row=1, column=5, columnspan=2, padx=10, sticky='we')
        self.label_beginn.grid(row=2, column=1, pady=5, padx=10, sticky='we')
        self.entry_beginn.grid(row=2, column=2, columnspan=2, padx=10, sticky='we')
        self.label_ende.grid(row=2, column=4, pady=10, padx=10, sticky='we')
        self.entry_ende.grid(row=2, column=5, columnspan=2, padx=10, sticky='we')
        self.label_notendurchschnitt_goal.grid(row=3, column=1, pady=5, padx=10, sticky='we')
        self.entry_notendurchschnitt_goal.grid(row=3, column=2, columnspan=2, padx=10, sticky='we')
        self.button_save_student.grid(row=3, column=6, padx=10, sticky='we')

        # module-Form Layout
        self.frame_module.pack(side='top', fill='both', expand=True, anchor='center')
        self.frame_module.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        self.frame_module.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        self.label_modul.grid(row=0, column=0, columnspan=2, padx=10, sticky='we')
        self.treeview_module.grid(row=1, rowspan=3, column=1, columnspan=3, padx=10, sticky='nwe')
        self.button_modul.grid(row=3, column=3, padx=10, sticky='we')
        self.button_zurueck.pack(side='left', pady=20, padx=20, anchor='w')

    def _note_pruefen(self, event):
        """Validiert die eingegebene Note und zeigt bei ungültigem Wert einen Fehler."""
        ergebnis = note_validieren(event)
        eingabe = str(event.value).strip()
        if ergebnis is None and eingabe != "":
            self.after_idle(
                lambda: messagebox.showerror(
                    "Ungültige Note",
                    "Bitte eine gültige Note eingeben.\n"
                    "Zahlen 1 bis 5.\n(zB. \"1.5\", \"1,5\" oder \"1\")"
                )
            )
        return ergebnis

    def _form_befuellen(self):
        """Befüllt die Formularfelder mit Student-Objekt im Bearbeitungsmodus."""
        self.entry_vorname.insert(0, self.student.vorname)
        self.entry_nachname.insert(0, self.student.nachname)
        self.entry_matrikelnummer.insert(0, self.student.matrikelnummer)
        self.str_var_studiengang.set(self.student.studiengang.studiengang)
        self.entry_notendurchschnitt_goal.insert(0, self.student.zielnotendurchschnitt)
        self.entry_beginn.set_date(self.student.beginndatum.date())
        self.entry_ende.set_date(self.student.zielabschlussdatum.date())
        self.button_modul.config(state='normal')

    def _combobox_befuellen(self):
        """Befüllt die Studiengang-Combobox mit allen Studiengängen."""
        self.studiengaenge = self.controller.studiengang_controller.lade_alle_studiengaenge()
        self.combobox_studiengang['values'] = [studiengang.studiengang for studiengang in self.studiengaenge]
        if self.studiengaenge:
            self.combobox_studiengang.current(0)

    def _treeview_befuellen(self):
        """Übeträgt Prüfungsleistungen des Studenten in das Noten-Sheet."""
        self.treeview_module.set_sheet_data([])
        sheet_data = []
        for pruefungsleistung in sorted(
                self.student.pruefungsleistungen,
                key=lambda x: x.modul.semester.semester
        ):
            note = "" if pruefungsleistung.note is None else pruefungsleistung.note
            sheet_data.append([
                pruefungsleistung.modul.modulname,
                pruefungsleistung.modul.modulcode,
                pruefungsleistung.modul.ects,
                pruefungsleistung.modul.semester.semester,
                note
            ])
        self.treeview_module.set_sheet_data(sheet_data, reset_col_positions=False)
        self.treeview_module.set_all_row_heights()

    def _combobox_auswahl(self) -> Studiengang | None:
        """Gibt den ausgewählten Studiengang zurück."""
        combobox_index = self.combobox_studiengang.current()
        if combobox_index == -1:
            return None
        return self.studiengaenge[combobox_index]

    def _student_speichern(self):
        """Prüft die Formularfelder und übergibt das Student-Objekt an den Controller.
        Wird im Bearbeitungsmodus der Studiengang gewechselt, wird eine Bestätigung erfordert,
        da alle bisherigen Prüfungsleistungen gelöscht werden.
        """
        studiengang = self._combobox_auswahl()

        # validierung
        if (
                self.entry_vorname.get() == "" or
                self.entry_nachname.get() == "" or
                self.entry_matrikelnummer.get() == "" or
                self.entry_beginn is None or
                self.entry_ende is None or
                self.entry_notendurchschnitt_goal.get() == "" or
                studiengang is None
        ):
            messagebox.showerror("Fehler", "Bitte füllen Sie alle Felder aus.")
            return
        if self.entry_ende.get_date() <= self.entry_beginn.get_date():
            messagebox.showerror("Fehler", "Das Enddatum muss größer als das Beginndatum sein.")
            return
        try:
            zielnotendurchschnitt = float(self.entry_notendurchschnitt_goal.get().strip().replace(',', '.'))
        except ValueError:
            messagebox.showerror("Fehler", "Bitte einen Zielnotendurchschnitt angeben.")
            return

        # Student aktualisieren.
        if self.edit:
            if studiengang.studiengang != self.student.studiengang.studiengang:
                msgbox = messagebox.askyesno(
                    'Studiengang geändert',
                    "Wenn der Studiengang geändert wird, "
                    "werden alle bisherigen Prüfungsleistungen des Studenten gelöscht!\n\n"
                    "Fortfahren?"
                )
                if not msgbox:
                    return

            student, fehler = self.controller.student_controller.student_aktualisieren(
                self.student,
                self.entry_vorname.get(),
                self.entry_nachname.get(),
                self.entry_matrikelnummer.get(),
                studiengang, zielnotendurchschnitt,
                self.entry_beginn.get_date(),
                self.entry_ende.get_date()
            )
        # Student anlegen.
        else:
            student, fehler = self.controller.student_controller.student_hinzufuegen(
                self.entry_vorname.get(),
                self.entry_nachname.get(),
                self.entry_matrikelnummer.get(),
                studiengang, zielnotendurchschnitt,
                self.entry_beginn.get_date(),
                self.entry_ende.get_date()
            )

        if fehler:
            messagebox.showerror("Fehler", fehler)
            self.controller.zeige_seite(Student_Verwalten, self.controller)
            return

        self.controller.zeige_seite(Student_Verwalten, self.controller)

    def _note_eintragen(self):
        """Übergibt das Noten-Sheet an den Controller und ladet das Formular neu."""
        data = self.treeview_module.get_sheet_data()
        pruefungsleistung, fehler = self.controller.student_controller.pruefungsleistungen_aktualisieren(
            self.student, data
        )
        if fehler:
            messagebox.showerror("Fehler", fehler)
            return
        self.controller.zeige_seite(StudentenForm, self.controller, student=self.student)