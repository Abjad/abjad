from abjad import *
import py.test


def test_GraceContainer_01():
    '''Grace music is a container.'''

    t = gracetools.GraceContainer([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])

    assert isinstance(t, Container)
    assert len(t) == 3
    assert t.lilypond_format == "\\grace {\n\tc'16\n\td'16\n\te'16\n}"

    r'''
    \grace {
        c'16
        d'16
        e'16
    }
    '''


def test_GraceContainer_02():
    '''GraceContainer.kind is managed attribute.
        GraceContainer.kind knows about "after", "grace",
        "acciaccatura", "appoggiatura"'''

    t = gracetools.GraceContainer([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])
    t.kind = 'acciaccatura'
    assert t.kind == 'acciaccatura'
    t.kind = 'grace'
    assert t.kind == 'grace'
    t.kind = 'after'
    assert t.kind == 'after'
    t.kind = 'appoggiatura'
    assert t.kind == 'appoggiatura'
    assert py.test.raises(AssertionError, 't.kind = "blah"')


def test_GraceContainer_03():
    '''Grace formats correctly as grace.'''

    t = gracetools.GraceContainer(notetools.make_repeated_notes(3))
    t.kind = 'grace'
    assert t.lilypond_format == "\\grace {\n\tc'8\n\tc'8\n\tc'8\n}"

    r'''
    \grace {
        c'8
        c'8
        c'8
    }
    '''


def test_GraceContainer_04():
    '''Grace formats correctly as acciaccatura.'''

    t = gracetools.GraceContainer(notetools.make_repeated_notes(3))
    t.kind = 'acciaccatura'
    assert t.lilypond_format == "\\acciaccatura {\n\tc'8\n\tc'8\n\tc'8\n}"

    r'''
    \acciaccatura {
        c'8
        c'8
        c'8
    }
    '''


def test_GraceContainer_05():
    '''Grace formats correctly as appoggiatura.'''

    t = gracetools.GraceContainer(notetools.make_repeated_notes(3))
    t.kind = 'appoggiatura'
    assert t.lilypond_format == "\\appoggiatura {\n\tc'8\n\tc'8\n\tc'8\n}"

    r'''
    \appoggiatura {
        c'8
        c'8
        c'8
    }
    '''


def test_GraceContainer_06():
    '''Grace formats correctly as after grace.'''

    t = gracetools.GraceContainer(notetools.make_repeated_notes(3))
    t.kind = 'after'
    assert t.lilypond_format == "{\n\tc'8\n\tc'8\n\tc'8\n}"

    r'''
    {
        c'8
        c'8
        c'8
    }
    '''


def test_GraceContainer_07():
    '''Grace containers can be appended.'''

    t = gracetools.GraceContainer(notetools.make_repeated_notes(2))
    n = Note(1, (1, 4))
    t.append(n)
    assert len(t) == 3
    assert t[-1] is n


def test_GraceContainer_08():
    '''Grace containers can be extended.'''

    t = gracetools.GraceContainer(notetools.make_repeated_notes(2))
    ns = Note(1, (1, 4)) * 2
    t.extend(ns)
    assert len(t) == 4
    assert t[-2:] == ns
