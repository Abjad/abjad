# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondproxytools_LilyPondGrobManager___delattr___01():

    note = Note("c'4")
    override(note).accidental.color = 'red'
    override(note).beam.positions = (-6, -6)
    override(note).dots.thicknes = 2

    assert testtools.compare(
        note,
        r'''
        \once \override Accidental #'color = #red
        \once \override Beam #'positions = #'(-6 . -6)
        \once \override Dots #'thicknes = #2
        c'4
        '''
        )

    del(override(note).accidental)
    del(override(note).beam)

    assert testtools.compare(
        note,
        r'''
        \once \override Dots #'thicknes = #2
        c'4
        '''
        )


def test_lilypondproxytools_LilyPondGrobManager___delattr___02():
    r'''Delete LilyPond Rest grob override.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    override(staff).rest.transparent = True
    del(override(staff).rest)

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


def test_lilypondproxytools_LilyPondGrobManager___delattr___03():
    r'''Delete LilyPond TimeSignature grob override.
    '''

    note = Note("c'4")
    override(note).time_signature.color = 'red'
    override(note).time_signature.transparent = True
    del(override(note).time_signature)

    assert note.lilypond_format == "c'4"
