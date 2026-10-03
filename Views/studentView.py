import ttkbootstrap as ttk
from tkinter import messagebox
import tkinter as tk
from tksheet import Sheet

from Model.student import Student
from Model.studiengang import Studiengang


class Student_Verwalten(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        # self.place(relx=0.5, rely=0.30, anchor="center", relwidth=0.7, relheight=0.8)
        self.create_widgets()
        self.fill_treeview()
        self.create_layout()

    def create_widgets(self):
        self.label_title = ttk.Label(self.parent, text="Studenten verwalten", font=("Arial", 24, 'bold'))

        self.treeview_studenten = ttk.Treeview(self, columns=('row', 'vorname', 'nachname', 'matrikelnummer', 'studiengang', 'notendurchschnitt_goal', 'beginn', 'ende'), show='headings')
        self.treeview_studenten.heading('row', text='Nr.', anchor='w')
        self.treeview_studenten.heading('vorname', text='Vorname', anchor='w')
        self.treeview_studenten.heading('nachname', text='Nachname', anchor='w')
        self.treeview_studenten.heading('matrikelnummer', text='Matrikelnummer', anchor='w')
        self.treeview_studenten.heading('studiengang', text='Studiengang', anchor='w')
        self.treeview_studenten.heading('notendurchschnitt_goal', text='Zielnotendurchschnitt', anchor='w')
        self.treeview_studenten.heading('beginn', text='Beginndatum', anchor='w')
        self.treeview_studenten.heading('ende', text='Enddatum', anchor='w')

        self.treeview_studenten.column('row', anchor='w', width=50)
        self.treeview_studenten.column('vorname', anchor='w', width=120)
        self.treeview_studenten.column('nachname', anchor='w', width=120)
        self.treeview_studenten.column('matrikelnummer', anchor='w', width=120)
        self.treeview_studenten.column('studiengang', anchor='w', width=280)
        self.treeview_studenten.column('notendurchschnitt_goal', anchor='w', width=150)
        self.treeview_studenten.column('beginn', anchor='w', width=120)
        self.treeview_studenten.column('ende', anchor='w')

        self.treeview_studenten.bind('<Delete>', lambda e: self.del_row())
        self.treeview_studenten.bind('<Double-Button-1>', lambda e: self.open_edit())

        # self.treeview_studenten.insert('', 0, values=('2',
        #                                                   'Manuel',
        #                                                   'Gschwent',
        #                                                   'Angewandte künstliche Intelligenz',
        #                                                   '2.5',
        #                                                   '02.12.2025',
        #                                                   '02.12.2029'))
        # self.treeview_studenten.insert('', 0, values=('1',
        #                                                   'Martin',
        #                                                   'Melendez-Treder',
        #                                                   'Arbeitslosigkeit',
        #                                                   '4',
        #                                                   '02.12.2026',
        #                                                   '02.12.2099'))

        self.style = ttk.Style()
        self.style.configure(
            "success.TButton",  # eigener Name
            font=("Helvetica", 18)
        )
        self.button_neu = ttk.Button(self, text='+', bootstyle='success', style='success.TButton', command= lambda: self.controller.zeige_seite(StudentenForm, self.controller))

        self.frame_buttons = ttk.Frame(self)
        self.button_bearbeiten = ttk.Button(self.frame_buttons, text="Datensatz bearbeiten", bootstyle='primary', command= self.open_edit)
        self.button_loeschen = ttk.Button(self.frame_buttons, text="Datensatz löschen", bootstyle='danger', command= self.del_row)
        self.button_zurueck = ttk.Button(self.frame_buttons, text="Zurück", bootstyle='secondary', command= lambda: self.controller.zeige_startseite())


    def create_layout(self):
        self.columnconfigure((0,1,2), weight=1, uniform='a')
        self.rowconfigure((0,1,2,3), weight=1, uniform='a')

        self.label_title.pack(side='top', pady=10, padx=10, fill='x', anchor='center')
        self.treeview_studenten.pack(side='top', pady=10, padx=10, fill='both', expand=True)
        self.button_neu.pack(side='top', pady=10, padx=10, anchor='center')
        self.frame_buttons.pack(side='top', pady=10, padx=10, fill='x', anchor='center')
        self.button_bearbeiten.pack(side='right', pady=10, padx=10, anchor='e')
        self.button_loeschen.pack(side='right', pady=10, padx=10, anchor='e')
        self.button_zurueck.pack(side='left', pady=10, padx=10, anchor='w')

    def fill_treeview(self):
        for item in self.treeview_studenten.get_children():
            self.treeview_studenten.delete(item)

        studenten = self.controller.student_controller.get_studenten()
        for nummer, student in enumerate(studenten, 1):
            beginn = student.beginndatum.strftime("%d.%m.%Y")
            ende = student.zielabschlussdatum.strftime("%d.%m.%Y")
            self.treeview_studenten.insert('', 'end', iid=str(student.matrikelnummer), values=(nummer, student.vorname, student.nachname, student.matrikelnummer, student.studiengang.studiengang, student.zielnotendurchschnitt, beginn, ende))

    def del_row(self):
        selection = self.treeview_studenten.selection()
        if not selection:
            return

        for item in selection:
            self.controller.student_controller.del_student(item)

        self.fill_treeview()

    def open_edit(self):
        student = self.controller.student_controller.get_student(self.treeview_studenten.selection()[0])
        self.controller.zeige_seite(StudentenForm, self.controller, student=student)

class StudentenForm(ttk.Frame):
    def __init__(self, parent, controller, student=None):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.student = student
        self.edit = student is not None
        self.studiengaenge = []
        # self.place(relx=0.5, rely=0.30, anchor="center", relwidth=0.7, relheight=0.8)
        self.create_widgets()
        self.fill_combobox()
        self.create_layout()

        if self.edit:
            self.fill_form()
            self.fill_treeview()

    def create_widgets(self):
        title = "Studenten bearbeiten" if self.edit else "Studenten anlegen"
        self.label_title = ttk.Label(self, text=title, font=("Arial", 24, "bold"))

        self.frame_studenten_form = ttk.Frame(self)
        self.label_vorname = ttk.Label(self.frame_studenten_form, text="Vorname:")
        self.entry_vorname = ttk.Entry(self.frame_studenten_form)
        self.label_nachname = ttk.Label(self.frame_studenten_form, text="Nachname:")
        self.entry_nachname = ttk.Entry(self.frame_studenten_form)
        self.label_matrikelnummer = ttk.Label(self.frame_studenten_form, text="Matrikelnummer:")
        self.entry_matrikelnummer = ttk.Entry(self.frame_studenten_form)
        self.label_studiengang = ttk.Label(self.frame_studenten_form, text="Studiengang:")
        self.str_var_studiengang = tk.StringVar()
        self.combobox_studiengang = ttk.Combobox(self.frame_studenten_form, textvariable=self.str_var_studiengang)
        self.label_notendurchschnitt_goal = ttk.Label(self.frame_studenten_form, text="Zielnotendurch-\nschnitt:")
        self.entry_notendurchschnitt_goal = ttk.Entry(self.frame_studenten_form)
        self.label_beginn = ttk.Label(self.frame_studenten_form, text="Beginndatum:")
        self.entry_beginn = ttk.DateEntry(self.frame_studenten_form)
        self.label_ende = ttk.Label(self.frame_studenten_form, text='Enddatum:')
        self.entry_ende = ttk.DateEntry(self.frame_studenten_form)
        self.button_save_student = ttk.Button(self.frame_studenten_form, text="Student speichern", bootstyle="primary", command=self.save_student)


        self.frame_module = ttk.Frame(self)
        self.label_modul = ttk.Label(self.frame_module, text="Module:", font=("Arial", 16, "bold"))
        self.treeview_module = Sheet(self.frame_module, headers=['Modulname', 'Modulcode', 'ECTS', 'Semester', 'Erreichte Note'], height=200)
        self.treeview_module.enable_bindings('edit_cell', 'single_select')
        self.treeview_module.readonly_columns([0,1,2,3])
        self.button_modul = ttk.Button(self.frame_module, text="Note Eintragen", bootstyle="primary", command=self.note_eintragen)

        self.button_zurueck = ttk.Button(self, text="Zurück", bootstyle='secondary', command= lambda: self.controller.zeige_seite(Student_Verwalten, self.controller))


    def create_layout(self):
        self.label_title.pack(side='top', pady=10, padx=10, fill='x', anchor='center')

        self.frame_studenten_form.pack(side='top', pady=10, padx=10, fill='both', anchor='center')
        self.frame_studenten_form.columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.frame_studenten_form.rowconfigure((0,1,2,3), weight=1, uniform='a')
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


        self.frame_module.pack(side='top', fill='both', expand=True, anchor='center')
        self.frame_module.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        self.frame_module.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        self.label_modul.grid(row = 0, column = 0, columnspan = 2, padx=10, sticky='we')
        self.treeview_module.grid(row = 1, rowspan=3, column = 1, columnspan = 3, padx=10, sticky='nwe')
        self.button_modul.grid(row = 3, column = 3, padx=10, sticky='we')

        self.button_zurueck.pack(side='left', pady=20, padx=20, anchor='w')


    def fill_form(self):
        self.entry_vorname.insert(0, self.student.vorname)
        self.entry_nachname.insert(0, self.student.nachname)
        self.entry_matrikelnummer.insert(0, self.student.matrikelnummer)
        self.str_var_studiengang.set(self.student.studiengang.studiengang)
        self.entry_notendurchschnitt_goal.insert(0, self.student.zielnotendurchschnitt)
        self.entry_beginn.set_date(self.student.beginndatum.date())
        self.entry_ende.set_date(self.student.zielabschlussdatum.date())

    def fill_combobox(self):
        self.studiengaenge = self.controller.studiengang_controller.get_studiengaenge()
        self.combobox_studiengang['values'] = [studiengang.studiengang for studiengang in self.studiengaenge]
        if self.studiengaenge:
            self.combobox_studiengang.current(0)

    def fill_treeview(self):
        self.treeview_module.set_sheet_data([])

        sheet_data = []

        for pruefungsleistung in self.student.pruefungsleistungen:
            note = "" if pruefungsleistung.note is None else pruefungsleistung.note
            sheet_data.append([pruefungsleistung.modul.modulname, pruefungsleistung.modul.modulcode, pruefungsleistung.modul.ects, pruefungsleistung.modul.semester.semester, note])

        self.treeview_module.set_sheet_data(sheet_data)

    def get_selected_item(self) -> Studiengang | None:
        combobox_index = self.combobox_studiengang.current()
        return self.studiengaenge[combobox_index]

    def save_student(self):
        studiengang = self.get_selected_item()

        if self.edit:
            if studiengang.studiengang != self.student.studiengang.studiengang:
                msgbox = messagebox.askyesno('Studiengang geändert','Wenn der Studiengang geändert wird, werden alle bisherigen Prüfungsleistungen des Studenten gelöscht!\n\nFortfahren?')
                if not msgbox:
                    return

            self.controller.student_controller.update_student(self.student, self.entry_vorname.get(), self.entry_nachname.get(), self.entry_matrikelnummer.get(), studiengang, self.entry_notendurchschnitt_goal.get(), self.entry_beginn.get_date(), self.entry_ende.get_date())
        else:
            self.controller.student_controller.add_student(self.entry_vorname.get(), self.entry_nachname.get(), self.entry_matrikelnummer.get(), studiengang, self.entry_notendurchschnitt_goal.get(), self.entry_beginn.get_date(), self.entry_ende.get_date())

        self.controller.zeige_seite(Student_Verwalten, self.controller)

    def note_eintragen(self):
        data = self.treeview_module.get_sheet_data()
        self.controller.student_controller.update_pruefungsleistungen(self.student, data)
        self.controller.zeige_seite(StudentenForm, self.controller, student=self.student)
