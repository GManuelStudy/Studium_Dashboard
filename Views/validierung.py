import re

# studiengang_validieren
def studiengang_validieren(studiengang: str):
    if len(studiengang) > 30:
        return False

    return re.fullmatch(
        r"[A-Za-zÄÖÜäöüß ]*",
        studiengang
    ) is not None

def ects_validieren(ects: str):
    if ects == "":
        return True
    if len(ects) > 2:
        return False
    return ects.isdigit()

def semester_validieren(semester: str):
    if semester == "":
        return True
    if len(semester) > 1:
        return False
    return semester.isdigit() and semester in "12345678"

def modulcode_validieren(modulcode: str):
    if len(modulcode) > 15:
        return False
    return re.fullmatch(
        r"[A-Za-zÄÖÜäöüß0-9]*",
        modulcode
    ) is not None

def modulname_validieren(modulname: str):
    if len(modulname) > 20:
        return False
    return re.fullmatch(
        r"[A-Za-zÄÖÜäöüß ]*",
        modulname
    ) is not None

# student validieren
def vorname_validieren(vorname: str):
    if len(vorname) > 15:
        return False
    return re.fullmatch(
        r"[A-Za-zÄÖÜäöüß]*",
        vorname
    ) is not None

def nachname_validieren(nachname: str):
    if len(nachname) > 15:
        return False
    return re.fullmatch(
        r"[A-Za-zÄÖÜäöüß]*",
        nachname
    ) is not None

def matrikelnummer_validieren(matrikelnummer: str):
    if len(matrikelnummer) > 10:
        return False
    return re.fullmatch(
        r"[A-Za-z0-9]*",
        matrikelnummer
    ) is not None

def beginndatum_validieren(beginndatum: str):
    if len(beginndatum) > 8:
        return False
    return re.fullmatch(
        r"[0-9/]*",
        beginndatum
    ) is not None

def zielabschlussdatum_validieren(zielabschlussdatum: str):
    if len(zielabschlussdatum) > 8:
        return False
    return re.fullmatch(
        r"[0-9/]*",
        zielabschlussdatum
    ) is not None

def zielnotendurchschnitt_validieren(zielnotendurchschnitt: str):
    if zielnotendurchschnitt == "":
        return True
    if not re.fullmatch(r"[1-4]([.,][0-9]?)?", zielnotendurchschnitt):
        return False
    return float(zielnotendurchschnitt.replace(',', '.')) <= 4.0

def note_validieren(event):
    note_text = str(event.value).strip().replace(',', '.')
    if note_text == "":
        return ""
    if not re.fullmatch(r"[1-5]([.,][0-9]?)?", note_text):
        return None
    if float(note_text) > 5.0:
        return None
    return note_text