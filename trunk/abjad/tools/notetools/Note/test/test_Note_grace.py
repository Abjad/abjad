from abjad import *


def test_Note_grace_01():
    '''Attach one grace note.
    '''

    note = Note("c'4")
    gracetools.Grace([Note(2, (1, 16))])(note)

    '''
    \grace {
        d'16
    }
    c'4
    '''

    assert note.format == "\\grace {\n\td'16\n}\nc'4"


def test_Note_grace_02():
    '''Attach several grace notes.
    '''

    note = Note("c'4")
    gracetools.Grace([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])(note)

    '''
    \grace {
        c'16
        d'16
        e'16
    }
    c'4
    '''

    assert note.format == "\\grace {\n\tc'16\n\td'16\n\te'16\n}\nc'4"


def test_Note_grace_03():
    '''Attach one appoggiatura.
    '''

    note = Note("c'4")
    gracetools.Grace([Note(2, (1, 16))], kind = 'appoggiatura')(note)

    r'''
    \appoggiatura {
        d'16
    }
    c'4
    '''

    assert note.format == "\\appoggiatura {\n\td'16\n}\nc'4"


def test_Note_grace_04():
    '''Attach one acciaccatura.
    '''

    note = Note("c'4")
    gracetools.Grace([Note(2, (1, 16))], kind = 'acciaccatura')(note)

    r'''
    \acciaccatura {
        d'16
    }
    c'4
    '''

    assert note.format == "\\acciaccatura {\n\td'16\n}\nc'4"


def test_Note_grace_05():
    '''Attach one after grace note.
    '''

    note = Note("c'4")
    gracetools.Grace([Note(2, (1, 16))], kind = 'after')(note)

    r'''
    \afterGrace
    c'4
    {
        d'16
    }
    '''

    assert note.format == "\\afterGrace\nc'4\n{\n\td'16\n}"


def test_Note_grace_06():
    '''Attach several after grace notes.
    '''

    note = Note("c'4")
    gracetools.Grace([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))], kind = 'after')(note)

    r'''
    \afterGrace
    c'4
    {
        c'16
        d'16
        e'16
    }
    '''

    assert note.format =="\\afterGrace\nc'4\n{\n\tc'16\n\td'16\n\te'16\n}"
