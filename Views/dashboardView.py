from tkinter import messagebox
import ttkbootstrap as ttk
import tkinter as tk
from DTO.pruefungsleistungDTO import PruefungsleistungDTO
from DTO.semesterDTO import SemesterDTO
from Model.status import Status


class Dashboard(ttk.Frame):
    """Dashboard View zur Anzeige des Dashboards"""
    def __init__(self, parent, controller):
        """Initialisiert das Dashboard-Fenster und verbindet die Controller-Klassen."""
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.dashboard_dto = None
        self._scroll_container_erstellen()
        self._widgets_erstellen()
        self._combobox_befuellen()
        self._init_layout_erstellen()

    def _widgets_erstellen(self):
        """Erstellt die grundlegenden Widgets des Dashboard-Fensters."""
        # titel
        self.frame_titel = ttk.Frame(self.scrollable_frame)
        self.label_titel = ttk.Label(
            self.frame_titel,
            text="Mein Dashboard",
            font=("Arial", 24, "bold")
        )
        self.str_var_benutzer = tk.StringVar(value='- Benutzer auswählen -')
        self.combobox_studenten = ttk.Combobox(
            self.frame_titel,
            state='readonly',
            textvariable=self.str_var_benutzer,
            width=50
        )
        self.label_sub_titel = ttk.Label(self.scrollable_frame, font=("Arial", 14))
        self.label_sub_titel2 = ttk.Label(self.scrollable_frame, font=("Arial", 12))

        # studienfortschritt
        self.frame_studienfortschritt = ttk.Frame(self.scrollable_frame)
        self.label_studienfortschritt = ttk.Label(
            self.frame_studienfortschritt,
            text="Studienfortschritt: ",
            font=("Arial", 10)
        )
        self.int_var_studienfortschritt = tk.IntVar()
        self.progressbar_studienfortschritt = ttk.Progressbar(
            self.frame_studienfortschritt,
            maximum=100,
            orient='horizontal',
            length=200,
            mode='determinate',
            variable=self.int_var_studienfortschritt
        )
        self.card_frame = ttk.Frame(self.scrollable_frame)
        # Durchschnittsnote und Studiendauer
        style = ttk.Style()
        style.configure("SdCard.TFrame", borderwidth=2, relief="solid", background="#ffffff")
        self.frame_mid = ttk.Frame(self.scrollable_frame)
        self.frame_durchschnittsnote = ttk.Frame(self.frame_mid)
        self.frame_studiendauer = ttk.Frame(self.frame_mid, style='SdCard.TFrame')
        self.label_durchschnittsnote = ttk.Label(
            self.frame_durchschnittsnote,
            text="Durchschnittsnote: 2.1",
            font=("Arial", 10)
        )
        self.label_zieldurschnittsnote = ttk.Label(
            self.frame_durchschnittsnote,
            text="Zielnote: 2",
            font=("Arial", 10)
        )
        self.label_mindestnote = ttk.Label(
            self.frame_durchschnittsnote,
            text="Mindestnote im nächsten Modul: 1.6",
            font=("Arial", 10)
        )
        self.label_durchschnitt_bei_mindestnote = ttk.Label(
            self.frame_durchschnittsnote,
            text="Durchschnittsnote wenn Mindestnote erreicht wird",
            font=("Arial", 8)
        )
        self.frame_studiendauer_top = ttk.Frame(self.frame_studiendauer)
        self.label_studiendauer = ttk.Label(
            self.frame_studiendauer_top,
            text="Studiendauer",
            font=("Arial", 10)
        )
        self.label_enddatum = ttk.Label(
            self.frame_studiendauer_top,
            text="Enddatum: 2024-06-30",
            font=("Arial", 10)
        )
        self.int_var_studiendauerfortschritt = tk.IntVar()
        self.progressbar_studiendauer = ttk.Progressbar(
            self.frame_studiendauer,
            maximum=100,
            orient='horizontal',
            length=200,
            mode='determinate',
            variable=self.int_var_studiendauerfortschritt
        )
        self.label_verbleibende_dauer = ttk.Label(
            self.frame_studiendauer,
            text="Verbleibende Studiendauer:",
            font=("Arial", 8)
        )
        self.label_verbleibende_dauer_value = ttk.Label(
            self.frame_studiendauer,
            text="2 Jahr(e), 10 Tage",
            font=("Arial", 8)
        )
        self.label_verfuegbare_dauer = ttk.Label(
            self.frame_studiendauer,
            text='Verfügbare Zeit pro Modul:',
            font=("Arial", 8)
        )
        self.label_verfuegbare_dauer_value = ttk.Label(
            self.frame_studiendauer,
            text="10 Tag(e)",
            font=("Arial", 8)
        )
        self.button_zurueck = ttk.Button(
            self.canvas,
            text='Zurück',
            bootstyle='secondary',
            command=lambda: self.controller.zeige_startseite()
        )

    def _init_layout_erstellen(self):
        """Erstellt das grundlegende Layout wenn man auf die Seite kommt."""
        self.frame_titel.pack(side='top', pady=5, padx=10, fill='x', anchor='center')
        self.label_titel.pack(side='left', pady=5, padx=10, fill='x', anchor='w')
        self.combobox_studenten.pack(side='right', padx=10, fill='x', anchor='e')
        self.combobox_studenten.bind('<<ComboboxSelected>>', self._combobox_auswahl_geaendert)
        self.button_zurueck.pack(side='bottom', pady=20, padx=20, anchor='sw')

    def _layout_erstellen(self):
        """Erstellt das Layout nach der Auswahl in der Combobox und dem Laden der Daten."""
        for widget in self.scrollable_frame.winfo_children():
            widget.pack_forget()

        self._init_layout_erstellen()
        # titel layout
        self.label_sub_titel.pack(side='top', padx=20, anchor='w')
        self.label_sub_titel2.pack(side='top', padx=20, anchor='w')

        # studienfortschritt progressbar layout
        self.frame_studienfortschritt.pack(side='top', padx=10, fill='x', anchor='center')
        self.frame_studienfortschritt.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')
        self.frame_studienfortschritt.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.label_studienfortschritt.grid(row=1, column=1, pady=5, columnspan=5, padx=10, sticky='we')
        self.progressbar_studienfortschritt.grid(row=2, column=1, columnspan=5, padx=10, sticky='we')

        # studienfortschritt karten layout
        self.card_frame.pack(side='top', padx=10, fill='x', anchor='center')
        self.card_frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        self.card_frame.rowconfigure(0, weight=1, uniform='a')
        self.card_ects.grid(row=0, column=1, pady=5, padx=10, sticky='nswe')
        self.card_semester.grid(row=0, column=2, pady=5, padx=10, sticky='nswe')
        self.card_module.grid(row=0, column=3, pady=5, padx=10, sticky='nswe')

        # durchschnittsnote layout
        self.frame_mid.pack(side='top', padx=10, pady=(5, 20), fill='x', anchor='center')
        self.frame_mid.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')
        self.frame_mid.rowconfigure(0, weight=1, uniform='a')
        self.frame_durchschnittsnote.grid(row=0, column=2, columnspan=2, pady=5, padx=10, sticky='nswe')
        self.frame_studiendauer.grid(row=0, column=4, columnspan=2, pady=5, padx=10, sticky='nswe')
        self.label_durchschnittsnote.pack(side='top', pady=(5,0), padx=10, fill='x', anchor='w')
        self.label_zieldurschnittsnote.pack(side='top', pady=(5,10), padx=10, fill='x', anchor='w')

        # studiendauer layout
        self.frame_studiendauer_top.pack(side='top', pady=5, padx=10, fill='x', anchor='w')
        self.label_studiendauer.pack(side='left', pady=5, padx=10, fill='x', anchor='w')
        self.label_enddatum.pack(side='right', pady=5, padx=10, fill='x', anchor='w')
        self.progressbar_studiendauer.pack(side='top', pady=5, padx=10, fill='x', anchor='w')
        self.label_verbleibende_dauer.pack(side='top', padx=10, fill='x', anchor='w')
        self.label_verbleibende_dauer_value.pack(side='top', pady=(0, 5), padx=10, fill='x', anchor='w')
        self.label_verfuegbare_dauer.pack(side='top', padx=10, fill='x', anchor='w')
        self.label_verfuegbare_dauer_value.pack(side='top', pady=(0, 5), padx=10, fill='x', anchor='w')

    def _lade_ausgewaehlten_student(self):
        """Lade den ausgewählten Studenten aus der Combobox."""
        index = self.combobox_studenten.current()
        if index == -1:
            return None

        student = self.studenten[index]
        student, fehler = self.controller.student_controller.lade_student(student.matrikelnummer)
        if fehler:
            messagebox.showerror("Fehler", fehler)
            self.controller.zeige_startseite()
            return None
        return student

    def _combobox_auswahl_geaendert(self, event):
        """Reagiert auf die Studentenauswahl und füllt die Form mit den Daten."""
        self.student = self._lade_ausgewaehlten_student()
        if self.student is None:
            self.controller.zeige_startseite()
            return
        self._form_befuellen()

    def _combobox_befuellen(self):
        """Befüllt die Combobox mit den Namen aller Studenten."""
        self.studenten = self.controller.student_controller.lade_alle_studenten()
        names = [
            f'{student.vorname} {student.nachname} - {student.matrikelnummer}'
            for student in self.studenten
        ]
        self.combobox_studenten['values'] = names

    def _form_befuellen(self):
        """Ladet das DashboardDTO und aktualisiert Karten, Kennzahlen und Semesteranzeigen."""
        # Back-Button wird neu erstellt und ans Layout angepasst.
        self.button_zurueck.destroy()
        self.button_zurueck = ttk.Button(
            self.scrollable_frame,
            text='Zurück',
            bootstyle='secondary',
            command=lambda: self.controller.zeige_startseite()
        )
        self.button_zurueck.pack(side='bottom', pady=20, padx=20, anchor='sw')
        self.dashboard_dto, fehler = self.controller.dashboard_controller.lade_dashboard_daten(
            self.student.matrikelnummer
        )
        if fehler:
            messagebox.showerror("Fehler", fehler)
            self.controller.zeige_startseite()
            return
        # titel aktualisieren
        self.label_sub_titel.config(
            text=f"{self.dashboard_dto.student.vorname} {self.dashboard_dto.student.nachname} -"
                 f" {self.dashboard_dto.student.matrikelnummer}"
        )
        self.label_sub_titel2.config(text=f"{self.dashboard_dto.studiengang.studiengang}")
        # Karten aktualisieren und befüllen
        self._studienfortschritt_befuellen()
        self._studiendauer_befuellen()
        self._layout_erstellen()
        self._durchschnittsnote_befuellen()
        self._semester_befuellen()

    def _studienfortschritt_befuellen(self):
        """Aktualisiert Fortschrittskennzahlen und setzt den Fortschrittsbalken."""
        dashboard_dto = self.dashboard_dto
        studienfortschritt = dashboard_dto.studienfortschritt
        self.int_var_studienfortschritt.set(studienfortschritt)
        self.label_studienfortschritt.config(text=f"Studienfortschritt: {studienfortschritt:.2f}%")
        self.card_ects = self._studienfortschritt_card_erstellen(
            'ECTS:',
            f'{dashboard_dto.student.aktuelleECTS} / {dashboard_dto.studiengang.ectsGesamt}'
        )
        self.card_semester = self._studienfortschritt_card_erstellen(
            'Semester:',
            f'{dashboard_dto.student.abgeschlosseneSemester} / {dashboard_dto.studiengang.anzahlSemester}'
        )
        self.card_module = self._studienfortschritt_card_erstellen(
            'Module:',
            f'{dashboard_dto.student.abgeschlosseneModule} / {dashboard_dto.studiengang.anzahlModule}'
        )

    def _durchschnittsnote_befuellen(self):
        """Aktualisiert Notendurchschnittskarte mit Ziel- und Ist-Werten.
        Ist der aktuelle Notendurchschnitt über dem Zielwert, so wird die Karte rot angezeigt und
        es wird die benötigte Mindestnote sowie der dadurch neu erreichte Notendurchschnitt
        angezeigt, um den Zielnotendurchschnitt zu erreichen.
        Ist der aktuelle Notendurchschnitt unter dem Zielwert, so wird die Karte grün angezeigt und
        die benötigte Mindestnote und der neue Notendurchschnitt werden nicht angezeigt.
        """
        dashboard_dto = self.dashboard_dto
        durschnittsnote = dashboard_dto.aktueller_notendurchschnitt
        zieldurschnittsnote = dashboard_dto.student.zielnotendurchschnitt
        erforderliche_note = dashboard_dto.erforderliche_note
        durchschnitt_neu = dashboard_dto.notendurchschnitt_bei_erfolgreicher_note
        style = ttk.Style()
        style.configure("GreenCard.TFrame", borderwidth=2, relief="solid", background="#d4edda")
        style.configure("RedCard.TFrame", borderwidth=2, relief="solid", background="#f8d7da")
        style.configure('RedLabel.TLabel', background='#f8d7da')
        style.configure('GreenLabel.TLabel', background='#d4edda')

        if durschnittsnote == 0:
            self.label_durchschnittsnote.config(text='Ø-Note: -')
        else:
            self.label_durchschnittsnote.config(text=f'Ø-Note: {durschnittsnote:.2f}')

        self.label_zieldurschnittsnote.config(text=f'Ziel Ø-Note: {zieldurschnittsnote:.2f}')
        if durschnittsnote <= zieldurschnittsnote:
            self.frame_durchschnittsnote.config(style='GreenCard.TFrame')
            self.label_durchschnittsnote.config(style='GreenLabel.TLabel')
            self.label_zieldurschnittsnote.config(style='GreenLabel.TLabel')
            self.label_mindestnote.pack_forget()
            self.label_durchschnitt_bei_mindestnote.pack_forget()
        else:
            self.frame_durchschnittsnote.config(style='RedCard.TFrame')
            self.label_durchschnittsnote.config(style='RedLabel.TLabel')
            self.label_zieldurschnittsnote.config(style='RedLabel.TLabel')
            self.label_mindestnote.config(style='RedLabel.TLabel')
            self.label_durchschnitt_bei_mindestnote.config(style='RedLabel.TLabel')
            self.label_mindestnote.config(
                text=f'Mindestnote im nächsten Modul: {erforderliche_note:.2f}'
            )
            self.label_durchschnitt_bei_mindestnote.config(
                text=f'Ø-Note wenn Mindestnote erreicht wird: {durchschnitt_neu:.2f}'
            )
            self.label_mindestnote.pack(side='top', pady=(5, 0), padx=10, fill='x', anchor='w')
            self.label_durchschnitt_bei_mindestnote.pack(side='top', pady=(5, 0), padx=10, fill='x', anchor='w')

    def _studiendauer_befuellen(self):
        """Aktualisiert Studiendauerkarte mit Fortschritt, Restzeit und Tage pro offenem Modul."""
        dashboard_dto = self.dashboard_dto
        fortschritt = dashboard_dto.studiendauer_fortschritt
        verbleibende_dauer = dashboard_dto.verbleibende_dauer
        self.label_studiendauer.config(text=f"Studiendauer: {fortschritt:.2f} %")
        self.label_enddatum.config(
            text=f"Enddatum: {dashboard_dto.student.zielabschlussdatum.strftime('%d.%m.%Y')}"
        )
        self.label_verbleibende_dauer_value.config(
            text=f"{verbleibende_dauer.years} Jahr(e), "
                 f"{verbleibende_dauer.months} Monat(e), "
                 f"{verbleibende_dauer.days} Tag(e)"
        )
        if dashboard_dto.verfuegbare_dauer_pro_modul is not None:
            self.label_verfuegbare_dauer_value.config(
                text=f'{dashboard_dto.verfuegbare_dauer_pro_modul:.2f} Tag(e)'
            )
        else:
            self.label_verfuegbare_dauer_value.config(text='N/A')
        self.int_var_studiendauerfortschritt.set(fortschritt)

    def _semester_befuellen(self):
        """Aktualisiert Semesterkarten und erstellt Accordions."""
        for semester in self.dashboard_dto.semester:
            self._accordion_erstellen(semester)

    def _module_befuellen(self, parent, modul_dto: PruefungsleistungDTO):
        """Erzeugt eine Modulzeile für Semesteranzeige aus ModulDTO."""
        modul = modul_dto.modul
        note = modul_dto.note

        if note is None or note == 0:
            note_text = '-'
        else:
            note_text = note

        content_row = tk.Frame(parent, bg='white', bd=1, relief='solid')
        content_row.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        content_row.rowconfigure(0, weight=1, uniform='a')
        ttk.Label(content_row, text=modul.modulname).grid(column=0, row=0, padx=20, sticky='w')
        ttk.Label(
            content_row,
            text=f'{modul.ects} ECTS',
            font=("Arial", 10)
        ).grid(column=1, row=0, padx=20)
        ttk.Label(
            content_row,
            text=f'Note: {note_text}',
            font=("Arial", 10)
        ).grid(column=2, row=0, padx=20)
        status_frame = ttk.Frame(content_row)
        status_frame.grid(column=3, row=0, padx=20)
        ttk.Label(status_frame, text='Status:', font=("Arial", 10)).pack(side='left')
        (self._status_label_erstellen(status_frame, modul_dto.status, font=("Arial", 10))
         .pack(side='left'))
        content_row.pack(fill="x", padx=20, pady=2)

    def _studienfortschritt_card_erstellen(self, label_title, label_wert):
        """Erzeugt eine Card aus Titel und Wert und gibt ihren Frame zurück"""
        style = ttk.Style()
        style.configure("Card.TFrame", borderwidth=2, relief="solid", background="#ffffff")
        self.card_studienfortschritt = ttk.Frame(self.card_frame, style="Card.TFrame")
        self.label_card = ttk.Label(self.card_studienfortschritt, text=label_title, font=("Arial", 10))
        self.label_wert = ttk.Label(self.card_studienfortschritt, text=label_wert, font=("Arial", 10))
        self.label_card.pack(side='top', pady=5, padx=10, fill='x', anchor='w')
        self.label_wert.pack(side='top', pady=5, padx=10, fill='x', anchor='w')
        return self.card_studienfortschritt

    def _accordion_erstellen(self, semester_dto: SemesterDTO, **kwargs):
        """Erzeugt ein aufklappbares Accordion für Semesteranzeige
        """
        # Eigener Container pro Accordion
        title = f'Semester {semester_dto.semester.semester}'
        note = semester_dto.notendurchschnitt
        status = semester_dto.status

        if note == 0:
            note_text = '-'
        else:
            note_text = f'{note:.2f}'

        container = tk.Frame(self.scrollable_frame, bd=1, relief='solid')
        container.pack(fill="x", padx=20, pady=3)

        header = tk.Frame(container, bg='white')
        header.pack(fill="x")

        label_header = ttk.Label(header, text=title, font=("Arial", 12))
        label_header2 = ttk.Label(header, text=f'Ø-Note: {note_text}', font=("Arial", 12))
        frame_header3 = ttk.Frame(header)
        label_header3 = ttk.Label(frame_header3, text=f'Status:', font=("Arial", 12))
        label_header3_value = self._status_label_erstellen(frame_header3, status)
        # if status == Status.OFFEN:
        #     label_header3 = ttk.Label(header, text=f'Status: {status}', font=("Arial", 12))
        # elif status == Status.ABGESCHLOSSEN:
        #     label_header3 = ttk.Label(header, text=f'Status: ✔', font=("Arial", 12))
        # elif status == Status.NICHT_BESTANDEN:
        #     label_header3 = ttk.Label(header, text=f'Status: ✘', font=("Arial", 12))
        label_header4 = ttk.Label(header, text='▼')

        header.columnconfigure((0, 1, 2), weight=2, uniform='a')
        header.columnconfigure(3, weight=1, uniform='a')
        header.rowconfigure(0, weight=1, uniform='a')

        label_header.grid(column=0, row=0, padx=20, sticky='w')
        label_header2.grid(column=1, row=0, padx=20)
        frame_header3.grid(column=2, row=0, padx=20)
        label_header3.pack(side='left', fill='x', anchor='w')
        label_header3_value.pack(side='left', fill='x', anchor='w')
        label_header4.grid(column=3, row=0, padx=15, sticky='e')

        content = ttk.Frame(container, padding=10)
        for item in semester_dto.pruefungsleistung:
            self._module_befuellen(content, item)

        # Zustand lokal je Accordion halten
        accordion_state = {'is_open': False}

        def _toggle_accordion(event=None, accordion_state=accordion_state, content=content):
            """Wechselt den Zustand des Accordions auf offen oder geschlossen."""
            if accordion_state['is_open']:
                content.pack_forget()
            else:
                content.pack(fill="x")
            accordion_state['is_open'] = not accordion_state['is_open']

        header.bind("<Button-1>", _toggle_accordion)
        label_header.bind("<Button-1>", _toggle_accordion)
        label_header2.bind("<Button-1>", _toggle_accordion)
        label_header3.bind("<Button-1>", _toggle_accordion)
        label_header4.bind("<Button-1>", _toggle_accordion)

        return container

    def _status_label_erstellen(self, parent, status, font=("Arial", 12)):
        """Zeigt bei 'Offen' den Text, sonst ein farbiges Icon."""
        if status == Status.OFFEN:
            return ttk.Label(parent, text=f'{status.value}', font=font)
        if status == Status.ABGESCHLOSSEN:
            return ttk.Label(parent, text='✔', foreground='#28a745', font=font)
        if status == Status.NICHT_BESTANDEN:
            return ttk.Label(parent, text='✘', foreground='#dc3545', font=font)
        return ttk.Label(parent, text=f'{status}', font=font)

    def _scroll_container_erstellen(self):
        """Erzeugt ein scrollbaren Container für die Dashboardanzeige.
        Das Canvas dient als scrollbarer Bereich und enthält einen inneren
        Frame, in dem die Dashboard-Inhalte platziert werden.

        Beim Ändern der Größe des inneren Frames wird die Scrollregion des
        Canvas aktualisiert.
        """
        # --- Canvas + Scrollbar bilden den äußeren scrollbaren Bereich. ---
        self.canvas = tk.Canvas(self, highlightthickness=0, background='white')
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set, confine=True)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        # Innerer Frame für Dashboard-Inhalte
        self.scrollable_frame = ttk.Frame(self.canvas, height=1000)
        self.scrollable_frame_id = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor='nw'
        )

        self.scrollable_frame.bind(
            "<Configure>",
            self._on_frame_configure
        )
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(self.scrollable_frame_id, width=event.width)
        )
        self.canvas.bind("<Enter>", lambda event: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))

    def _on_mousewheel(self, event):
        """Scrollt den vorhandenen Canvas."""
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    def _on_frame_configure(self, event=None):
        """Passt den Scrollbereich an die Größe des inneren Frames an."""
        width = self.canvas.winfo_width()
        height = max(self.scrollable_frame.winfo_reqheight(), self.canvas.winfo_height())
        self.canvas.configure(scrollregion=(0, 0, width, height))