from abjad import *


def test_LilyPondGrobOverrideComponentPlugIn___delattr___01():

    note = Note("c'4")
    note.override.accidental.color = 'red'
    note.override.beam.positions = (-6, -6)
    note.override.dots.thicknes = 2

    r'''
    \once \override Accidental #'color = #red
    \once \override Beam #'positions = #'(-6 . -6)
    \once \override Dots #'thicknes = #2
    c'4
    '''

    del(note.override.accidental)
    del(note.override.beam)

    r'''
    \once \override Dots #'thicknes = #2
    c'4
    '''

    assert note.format == "\\once \\override Dots #'thicknes = #2\nc'4"


def test_LilyPondGrobOverrideComponentPlugIn___delattr___02():
    '''Delete LilyPond Rest grob override.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.rest.transparent = True
    del(t.override.rest)

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___delattr___03():
    '''Delete LilyPond TimeSignature grob override.
    '''

    t = Note("c'4")
    t.override.time_signature.color = 'red'
    t.override.time_signature.transparent = True
    del(t.override.time_signature)

    assert t.format == "c'4"
