from tkinter import messagebox

import ttkbootstrap as ttk
import tkinter as tk

from DTO.modulDTO import ModulDTO
from DTO.semesterDTO import SemesterDTO
from Model.status import Status
from Model.student import Student
from Model.studiengang import Studiengang


class Dashboard(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.dashboard_dto = None
        # self.place(relx=0.5, rely=0.30, anchor="center", relwidth=0.7, relheight=0.8)
        self.create_scroll_container()
        self.create_widgets()
        self.fill_combobox()
        self.create_init_layout()

    def create_widgets(self):
        # titel
        self.frame_title = ttk.Frame(self.scrollable_frame)
        self.label_title = ttk.Label(self.frame_title, text="Mein Dashboard", font=("Arial", 24, "bold"))
        self.str_var_benutzer = tk.StringVar(value='- Benutzer auswählen -')
        self.combobox_studenten = ttk.Combobox(self.frame_title, state='readonly', textvariable=self.str_var_benutzer, width=50)
        self.label_sub_title = ttk.Label(self.scrollable_frame, font=("Arial", 14))
        self.label_sub_title2 = ttk.Label(self.scrollable_frame, font=("Arial", 12))

        # studienfortschritt
        self.frame_studienfortschritt = ttk.Frame(self.scrollable_frame)
        self.label_studienfortschritt = ttk.Label(self.frame_studienfortschritt, text="Studienfortschritt: ", font=("Arial", 10))
        self.int_var_studienfortschritt = tk.IntVar()
        self.progressbar_studienfortschritt = ttk.Progressbar(self.frame_studienfortschritt, maximum=100, orient='horizontal', length=200, mode='determinate', variable=self.int_var_studienfortschritt)

        self.card_frame = ttk.Frame(self.scrollable_frame)

        # Durchschnittsnote und Studiendauer
        style = ttk.Style()
        style.configure("SdCard.TFrame", borderwidth=2, relief="solid", background="#ffffff")
        self.frame_mid = ttk.Frame(self.scrollable_frame)
        self.frame_durchschnittsnote = ttk.Frame(self.frame_mid)
        self.frame_studiendauer = ttk.Frame(self.frame_mid, style='SdCard.TFrame')

        self.label_durchschnittsnote = ttk.Label(self.frame_durchschnittsnote, text="Durchschnittsnote: 2.1", font=("Arial", 10))
        self.label_zieldurschnittsnote = ttk.Label(self.frame_durchschnittsnote, text="Zielnote: 2", font=("Arial", 10))
        self.label_mindestnote = ttk.Label(self.frame_durchschnittsnote, text="Mindestnote im nächsten Modul: 1.6", font=("Arial", 10))
        self.label_durchschnitt_bei_mindestnote = ttk.Label(self.frame_durchschnittsnote, text="Durchschnittsnote wenn Mindestnote erreicht wird", font=("Arial", 8))

        self.frame_studiendauer_top = ttk.Frame(self.frame_studiendauer)
        self.label_studiendauer = ttk.Label(self.frame_studiendauer_top, text="Studiendauer", font=("Arial", 10))
        self.label_enddatum = ttk.Label(self.frame_studiendauer_top, text="Enddatum: 2024-06-30", font=("Arial", 10))
        self.int_var_studiendauerfortschritt = tk.IntVar()
        self.progressbar_studiendauer  = ttk.Progressbar(self.frame_studiendauer, maximum=100, orient='horizontal', length=200, mode='determinate', variable=self.int_var_studiendauerfortschritt)
        self.label_verbleibende_dauer = ttk.Label(self.frame_studiendauer, text="Verbleibende Studiendauer:", font=("Arial", 8))
        self.label_verbleibende_dauer_value = ttk.Label(self.frame_studiendauer, text="2 Jahr(e), 10 Tage", font=("Arial", 8))
        self.label_verfuegbare_dauer = ttk.Label(self.frame_studiendauer, text='Verfügbare Zeit pro Modul:', font=("Arial", 8))
        self.label_verfuegbare_dauer_value = ttk.Label(self.frame_studiendauer, text="10 Tag(e)", font=("Arial", 8))

        self.button_back = ttk.Button(self.canvas, text='Zurück', bootstyle='secondary', command= lambda: self.controller.zeige_startseite())

    def create_init_layout(self):
        self.frame_title.pack(side='top', pady=5, padx=10, fill='x', anchor='center')
        self.label_title.pack(side='left', pady=5, padx=10, fill='x', anchor='w')
        self.combobox_studenten.pack(side='right', padx=10, fill='x', anchor='e')
        self.combobox_studenten.bind('<<ComboboxSelected>>', self.combobox_change_selected)
        self.button_back.pack(side='bottom', pady=20, padx=20, anchor='sw')


    def create_layout(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.pack_forget()

        self.create_init_layout()
        self.label_sub_title.pack(side='top', padx=20, anchor='w')
        self.label_sub_title2.pack(side='top', padx=20, anchor='w')

        self.frame_studienfortschritt.pack(side='top', padx=10, fill='x', anchor='center')
        self.frame_studienfortschritt.columnconfigure((0,1,2,3,4,5,6), weight=1, uniform='a')
        self.frame_studienfortschritt.rowconfigure((0,1,2,3), weight=1, uniform='a')
        self.label_studienfortschritt.grid(row=1, column=1, pady=5, columnspan=5, padx=10, sticky='we')
        self.progressbar_studienfortschritt.grid(row=2, column=1, columnspan=5, padx=10, sticky='we')

        self.card_frame.pack(side='top', padx=10, fill='x', anchor='center')
        self.card_frame.columnconfigure((0,1,2,3,4), weight=1, uniform='a')
        self.card_frame.rowconfigure(0, weight=1, uniform='a')
        self.card_ects.grid(row=0, column=1, pady=5, padx=10, sticky='nswe')
        self.card_semester.grid(row = 0, column=2, pady=5, padx=10, sticky='nswe')
        self.card_module.grid(row = 0, column=3, pady=5, padx=10, sticky='nswe')

        self.frame_mid.pack(side='top', padx=10, pady=(5,20), fill='x', anchor='center')
        self.frame_mid.columnconfigure((0,1,2,3,4,5,6), weight=1, uniform='a')
        self.frame_mid.rowconfigure(0, weight=1, uniform='a')
        self.frame_durchschnittsnote.grid(row=0, column=2, columnspan=2, pady=5, padx=10, sticky='nswe')
        self.frame_studiendauer.grid(row=0, column=4, columnspan=2, pady=5, padx=10, sticky='nswe')
        self.label_durchschnittsnote.pack(side='top', pady=5, padx=10, fill='x', anchor='w')
        self.label_zieldurschnittsnote.pack(side='top', pady=5, padx=10, fill='x', anchor='w')


        self.frame_studiendauer_top.pack(side='top', pady=5, padx=10, fill='x', anchor='w')
        self.label_studiendauer.pack(side='left', pady=5, padx=10, fill='x', anchor='w')
        self.label_enddatum.pack(side='right', pady=5, padx=10, fill='x', anchor='w')
        self.progressbar_studiendauer.pack(side='top', pady=5, padx=10, fill='x', anchor='w')
        self.label_verbleibende_dauer.pack(side='top', padx=10, fill='x', anchor='w')
        self.label_verbleibende_dauer_value.pack(side='top', pady=(0,5), padx=10, fill='x', anchor='w')
        self.label_verfuegbare_dauer.pack(side='top', padx=10, fill='x', anchor='w')
        self.label_verfuegbare_dauer_value.pack(side='top', pady=(0,5), padx=10, fill='x', anchor='w')

    def get_selected_student(self):
        index = self.combobox_studenten.current()

        if index == -1:
            return None

        student = self.studenten[index]
        student, fehler = self.controller.dashboard_controller.get_student(student.matrikelnummer)
        if fehler:
            messagebox.showerror("Fehler", fehler)
            self.controller.zeige_startseite()
            return None
        return student

    def combobox_change_selected(self, event):
        self.student = self.get_selected_student()
        if self.student is None:
            self.controller.zeige_startseite()
            return
        self.fill_form()

    def fill_combobox(self):
        self.studenten = self.controller.dashboard_controller.get_studenten()
        names = [f'{student.vorname} {student.nachname} - {student.matrikelnummer}' for student in self.studenten]
        self.combobox_studenten['values'] = names

    def fill_form(self):
        # back button
        self.button_back.destroy()
        self.button_back = ttk.Button(self.scrollable_frame, text='Zurück', bootstyle='secondary',command=lambda: self.controller.zeige_startseite())
        self.button_back.pack(side='bottom', pady=20, padx=20, anchor='sw')

        self.dashboard_dto, fehler = self.controller.dashboard_controller.lade_dashboard_daten(
            self.student.matrikelnummer
        )

        if fehler:
            messagebox.showerror("Fehler", fehler)
            self.controller.zeige_startseite()
            return

        self.label_sub_title.config(text=f"{self.dashboard_dto.student.vorname} {self.dashboard_dto.student.nachname} - {self.dashboard_dto.student.matrikelnummer}")
        self.label_sub_title2.config(text=f"{self.dashboard_dto.studiengang.studiengang}")
        self.fill_studienfortschritt()

        self.fill_studiendauer()
        self.create_layout()
        self.fill_durchschnittsnote()
        self.fill_semester()

    def fill_studienfortschritt(self):
        dashboard_dto = self.dashboard_dto
        studienfortschritt = dashboard_dto.studienfortschritt
        self.int_var_studienfortschritt.set(studienfortschritt)
        self.label_studienfortschritt.config(text=f"Studienfortschritt: {studienfortschritt:.2f}%")
        self.card_ects = self.create_studienfortschritt_card('ECTS:', f'{dashboard_dto.student.aktuelleECTS} / {dashboard_dto.studiengang.ectsGesamt}')
        self.card_semester = self.create_studienfortschritt_card('Semester:', f'{dashboard_dto.student.abgeschlosseneSemester} / {dashboard_dto.studiengang.anzahlSemester}')
        self.card_module = self.create_studienfortschritt_card('Module:', f'{dashboard_dto.student.abgeschlosseneModule} / {dashboard_dto.studiengang.anzahlModule}')

    def fill_durchschnittsnote(self):
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
            self.label_mindestnote.config(text=f'Mindestnote im nächsten Modul: {erforderliche_note:.2f}')
            self.label_durchschnitt_bei_mindestnote.config(text=f'Ø-Note wenn Mindestnote erreicht wird: {durchschnitt_neu:.2f}')
            self.label_mindestnote.pack(side='top', pady=(5,0), padx=10, fill='x', anchor='w')
            self.label_durchschnitt_bei_mindestnote.pack(side='top', pady=(5,0), padx=10, fill='x', anchor='w')

    def fill_studiendauer(self):
        dashboard_dto = self.dashboard_dto
        fortschritt = dashboard_dto.studiendauer_fortschritt
        verbleibende_dauer = dashboard_dto.verbleibende_dauer
        self.label_studiendauer.config(text=f"Studiendauer: {fortschritt:.2f} %")
        self.label_enddatum.config(text=f"Enddatum: {dashboard_dto.student.zielabschlussdatum.strftime('%d.%m.%Y')}")
        self.label_verbleibende_dauer_value.config(text=f'{verbleibende_dauer.years} Jahr(e), {verbleibende_dauer.months} Monat(e), {verbleibende_dauer.days} Tag(e)')
        if dashboard_dto.verfuegbare_dauer_pro_modul is not None:
            self.label_verfuegbare_dauer_value.config(text=f'{dashboard_dto.verfuegbare_dauer_pro_modul:.2f} Tag(e)')
        else:
            self.label_verfuegbare_dauer_value.config(text='N/A')
        self.int_var_studiendauerfortschritt.set(fortschritt)

    def fill_semester(self):
        for semester in self.dashboard_dto.semester:
            self.create_accordion(semester)

    def fill_module(self, parent, modul_dto: ModulDTO):
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
        ttk.Label(content_row, text=f'{modul.ects} ECTS', font=("Arial", 10)).grid(column=1, row=0, padx=20)
        ttk.Label(content_row, text=f'Note: {note_text}', font=("Arial", 10)).grid(column=2, row=0, padx=20)
        ttk.Label(content_row, text=f'Status: {modul_dto.status}', font=("Arial", 10)).grid(column=3, row=0, padx=20)
        content_row.pack(fill="x", padx=20, pady=2)



    def create_studienfortschritt_card(self, label_title, label_value):
        style = ttk.Style()
        style.configure("Card.TFrame", borderwidth=2, relief="solid", background="#ffffff")
        self.card_studienfortschritt = ttk.Frame(self.card_frame, style="Card.TFrame")
        self.label_card = ttk.Label(self.card_studienfortschritt, text=label_title, font=("Arial", 10))
        self.label_value = ttk.Label(self.card_studienfortschritt, text=label_value, font=("Arial", 10))
        self.label_card.pack(side='top', pady=5, padx=10, fill='x', anchor='w')
        self.label_value.pack(side='top', pady=5, padx=10, fill='x', anchor='w')
        return self.card_studienfortschritt

    def create_accordion(self, semester_dto: SemesterDTO, **kwargs):
        # Eigener Container pro Accordion – hält Header + Content zusammen
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
        label_header3 = ttk.Label(header, text=f'Status: {status}', font=("Arial", 12))
        label_header4 = ttk.Label(header, text='▼')

        header.columnconfigure((0, 1, 2), weight=2, uniform='a')
        header.columnconfigure(3, weight=1, uniform='a')
        header.rowconfigure(0, weight=1, uniform='a')
        label_header.grid(column=0, row=0, padx=20, sticky='w')
        label_header2.grid(column=1, row=0, padx=20)
        label_header3.grid(column=2, row=0, padx=20)
        label_header4.grid(column=3, row=0, padx=15, sticky='e')

        content = ttk.Frame(container, padding=10)

        for item in semester_dto.module:
            self.fill_module(content, item)
            # content_row = tk.Frame(content, bg='white', bd=1, relief='solid')
            # content_row.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
            # content_row.rowconfigure(0, weight=1, uniform='a')
            # ttk.Label(content_row, text=f"Inhalte von {title}").grid(column=0, row=0, padx=20, sticky='w')
            # ttk.Label(content_row, text=f"Inhalte von {title}", font=("Arial", 10)).grid(column=1, row=0, padx=20)
            # ttk.Label(content_row, text=f"Inhalte von {title}", font=("Arial", 10)).grid(column=2, row=0, padx=20)
            # ttk.Label(content_row, text=f"Inhalte von {title}", font=("Arial", 10)).grid(column=3, row=0, padx=20)
            # content_row.pack(fill="x", padx=20, pady=2)

        # Zustand lokal je Accordion halten (nicht auf self!)
        accordion_state = {'is_open': False}

        def toggle(event=None, accordion_state=accordion_state, content=content):
            if accordion_state['is_open']:
                content.pack_forget()
            else:
                content.pack(fill="x")
            accordion_state['is_open'] = not accordion_state['is_open']

        header.bind("<Button-1>", toggle)
        label_header.bind("<Button-1>", toggle)
        label_header2.bind("<Button-1>", toggle)
        label_header3.bind("<Button-1>", toggle)
        label_header4.bind("<Button-1>", toggle)

        return container

    def create_scroll_container(self):
        # --- Canvas + Scrollbar tragen das GESAMTE Fenster ---
        self.canvas = tk.Canvas(self, highlightthickness=0, background='white')
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set, confine=True)

        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        # Innerer Frame, der ALLES aufnimmt (Titel + Rest)
        self.scrollable_frame = ttk.Frame(self.canvas, height=1000)
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        self.scrollable_frame.bind(
            "<Configure>",
            self._on_frame_configure
        )
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(self.scrollable_frame_id, width=event.width))
        self.canvas.bind("<Enter>", lambda event: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))

    def _on_mousewheel(self, event):
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    def _on_frame_configure(self, event=None):
        width = self.canvas.winfo_width()
        height = max(self.scrollable_frame.winfo_reqheight(), self.canvas.winfo_height())
        self.canvas.configure(scrollregion=(0, 0, width, height))