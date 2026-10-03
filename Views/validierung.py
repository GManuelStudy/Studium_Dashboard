import re

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
        r"[A-Za-zÄÖÜäöüß0-9 ]*",
        modulcode
    ) is not None

def modulname_validieren(modulname: str):
    if len(modulname) > 20:
        return False
    return re.fullmatch(
        r"[A-Za-zÄÖÜäöüß ]*",
        modulname
    ) is not None