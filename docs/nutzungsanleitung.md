# Nutzungsanleitung – Studium Dashboard

**Anmerkung:** Diese Nutzungsanleitung wurde KI generiert und vom Studierenden, Manuel Gschwent auf 
Richtigkeit überprüft und angepasst.

Das Studium Dashboard verwaltet Studiengänge, Studenten und Modulnoten und zeigt
den persönlichen Studienfortschritt. Voraussetzung ist die abgeschlossene
Installation gemäß der Installationsanleitung.

### 1. Start und Navigation

Die virtuelle Umgebung aktivieren und im Projektordner `python main.py` ausführen.
Die Startseite bietet **Studiengänge verwalten**, **Studenten verwalten** und
**Zum Dashboard**. Bei einer leeren Datenbank zunächst die Schritte 2 und 3 durchführen.

### 2. Studiengang und Module anlegen

**Studiengänge verwalten → +** öffnen, die Studiengangbezeichnung eingeben und
**Studiengang speichern** wählen. Anschließend werden die Moduleingaben freigeschaltet.
Für jedes Modul **Modulname**, **Modulcode**, **ECTS** und **Semester** eintragen
und **Hinzufügen** anklicken. Der Modulcode muss innerhalb des Studiengangs eindeutig
sein. Die Semesternummer liegt zwischen 1 und 12. Semester werden automatisch angelegt.

Vorhandene Studiengänge per Doppelklick oder über **Datensatz bearbeiten** öffnen.
Dort kanns man die Bezeichnung ändern, Module hinzufügen oder ein ausgewähltes
Modul mit **Modul löschen** entfernen.

### 3. Studenten anlegen und bearbeiten

**Studenten verwalten → +** öffnen. Vorname, Nachname und eindeutige Matrikelnummer
eintragen, den Studiengang auswählen und den **Zielnotendurchschnitt** zwischen
1 und 4 festlegen. Beginn und geplantes Ende über die Kalender auswählen.
Das Enddatum muss nach dem Beginndatum liegen. Mit **Student speichern** abschließen.

Zum Bearbeiten den Studenten in der Übersicht doppelt anklicken oder markieren
und **Datensatz bearbeiten** wählen. Änderungen an den Stammdaten mit
**Student speichern** übernehmen. Ein bestätigter Studiengangwechsel löscht die
bisherigen Prüfungsleistungen und legt die Prüfungsleistungen neu an.

### 4. Noten eintragen

Den gespeicherten Studenten im Bearbeitungsmodus öffnen. In der Modultabelle die
Zelle **Erreichte Note** bearbeiten, beispielsweise per Doppelklick.
Zulässig sind Noten von **1 bis 5** mit höchstens einer Dezimalstelle.
Punkt und Komma sind möglich, etwa `2.3` oder `2,3`.
Eine leere Zelle kennzeichnet eine offene Prüfung.
Die Eingabe abschließen und mit **Note Eintragen** speichern.

### 5. Dashboard ansehen und Daten verwalten

**Zum Dashboard** öffnen und einen Studenten auswählen. Die Anzeige enthält
erreichte ECTS, abgeschlossene Module und Semester, Studienfortschritt,
aktuellen und angestrebten Notendurchschnitt sowie Restzeit bis zum geplanten Abschluss.
Bei einem schlechteren Durchschnitt als dem Zielwert erscheinen zusätzlich eine
berechnete Note für das nächste Modul und der daraus folgende Durchschnitt.

Semesterüberschriften anklicken, um Module, Noten und Status aufzuklappen:
**Offen** = ohne Note, **✔** = bestanden (1 bis 4), **✘** = nicht bestanden (über 4).
Weitere Inhalte sind durch Scrollen erreichbar.

Studenten und Studiengänge lassen sich in ihrer Übersicht über **Datensatz löschen**
entfernen. Ein Studiengang mit zugeordneten Studenten kann nicht gelöscht werden.
Das Löschen eines Studenten oder Moduls entfernt auch die zugehörigen Prüfungsleistungen.