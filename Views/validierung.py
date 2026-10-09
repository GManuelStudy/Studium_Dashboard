import re

# studiengang_validieren
def studiengang_validieren(studiengang: str):
    """Erlaubt bis zu 60 Buchstaben, Umlaute oder Leerzeichen, auch leeren Text."""
    if len(studiengang) > 60:
        return False

    return re.fullmatch(
        r"[A-Za-zÄÖÜäöüß ]*",
        studiengang
    ) is not None

def ects_validieren(ects: str):
    """Erlaubt bis zu 2 Ziffern, auch leeren Text."""
    if ects == "":
        return True
    if len(ects) > 2:
        return False
    return ects.isdigit()

def semester_validieren(semester: str):
    """Erlaubt eine Ziffer von 1 bis 8, auch leeren Text."""
    if semester == "":
        return True
    return semester.isdigit() and 1 <= int(semester) <= 12

def modulcode_validieren(modulcode: str):
    """Erlaubt bis zu 20 Buchstaben, Ziffern oder Umlaute, auch leeren Text."""
    if len(modulcode) > 20:
        return False
    return re.fullmatch(
        r"[A-Za-zÄÖÜäöüß0-9:_/. -]*",
        modulcode
    ) is not None

def modulname_validieren(modulname: str):
    """Erlaubt bis zu 100 Buchstaben, Umlaute oder Leerzeichen, auch leeren Text."""
    if len(modulname) > 100:
        return False
    return re.fullmatch(
        r"[A-Za-zÄÖÜäöüß:_ -]*",
        modulname
    ) is not None

# student validieren
def vorname_validieren(vorname: str):
    """Erlaubt bis zu 20 Buchstaben oder Umlaute, auch leeren Text."""
    if len(vorname) > 20:
        return False
    return re.fullmatch(
        r"[A-Za-zÄÖÜäöüß]*",
        vorname
    ) is not None

def nachname_validieren(nachname: str):
    """Erlaubt bis zu 30 Buchstaben oder Umlaute, auch leeren Text."""
    if len(nachname) > 30:
        return False
    return re.fullmatch(
        r"[A-Za-zÄÖÜäöüß]*",
        nachname
    ) is not None

def matrikelnummer_validieren(matrikelnummer: str):
    """Erlaubt bis zu 10 Buchstaben oder Ziffern, auch leeren Text."""
    if len(matrikelnummer) > 10:
        return False
    return re.fullmatch(
        r"[A-Za-z0-9]*",
        matrikelnummer
    ) is not None

def beginndatum_validieren(beginndatum: str):
    """Erlaubt ein Datum im Format dd/mm/yyyy."""
    if len(beginndatum) > 8:
        return False
    return re.fullmatch(
        r"[0-9/]*",
        beginndatum
    ) is not None

def zielabschlussdatum_validieren(zielabschlussdatum: str):
    """Erlaubt ein Datum im Format dd/mm/yyyy."""
    if len(zielabschlussdatum) > 8:
        return False
    return re.fullmatch(
        r"[0-9/]*",
        zielabschlussdatum
    ) is not None

def zielnotendurchschnitt_validieren(zielnotendurchschnitt: str):
    """Erlaubt leeren Text oder Zielnoten 1 bis 4 mit höchstens einer Dezimalstelle."""
    if zielnotendurchschnitt == "":
        return True
    if not re.fullmatch(r"[1-4]([.,][0-9]?)?", zielnotendurchschnitt):
        return False
    return float(zielnotendurchschnitt.replace(',', '.')) <= 4.0

def note_validieren(event):
    """Validiert event.value bei der Bearbeitung einer tksheet-Notenzelle.
    Liefert normalisierten Text mit Dezimalpunkt, leeren Text zum Löschen oder
    None zum Ablehnen. Zulässig sind Noten 1 bis 5 mit einer Dezimalstelle.
    """
    note_text = str(event.value).strip().replace(',', '.')
    if note_text == "":
        return ""
    if not re.fullmatch(r"[1-5]([.,][0-9]?)?", note_text):
        return None
    if float(note_text) > 5.0:
        return None
    return note_text