# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondproxytools_LilyPondGrobOverrideComponentPlugIn___delattr___01():

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

    assert testtools.compare(
        note,
        r'''
        \once \override Dots #'thicknes = #2
        c'4
        '''
        )


def test_lilypondproxytools_LilyPondGrobOverrideComponentPlugIn___delattr___02():
    r'''Delete LilyPond Rest grob override.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.rest.transparent = True
    del(staff.override.rest)

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )


def test_lilypondproxytools_LilyPondGrobOverrideComponentPlugIn___delattr___03():
    r'''Delete LilyPond TimeSignature grob override.
    '''

    note = Note("c'4")
    note.override.time_signature.color = 'red'
    note.override.time_signature.transparent = True
    del(note.override.time_signature)

    assert note.lilypond_format == "c'4"
