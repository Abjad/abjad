# -*- coding: utf-8 -*-
from abjad import *


def test_lilypondproxytools_LilyPondGrobNameManager___delattr___01():

    note = Note("c'4")
    override(note).accidental.color = 'red'
    override(note).beam.positions = (-6, -6)
    override(note).dots.thicknes = 2

    assert format(note) == stringtools.normalize(
        r'''
        \once \override Accidental.color = #red
        \once \override Beam.positions = #'(-6 . -6)
        \once \override Dots.thicknes = #2
        c'4
        '''
        )

    del(override(note).accidental)
    del(override(note).beam)

    assert format(note) == stringtools.normalize(
        r'''
        \once \override Dots.thicknes = #2
        c'4
        '''
        )


def test_lilypondproxytools_LilyPondGrobNameManager___delattr___02():
    r'''Delete LilyPond Rest grob override.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    override(staff).rest.transparent = True
    del(override(staff).rest)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )


def test_lilypondproxytools_LilyPondGrobNameManager___delattr___03():
    r'''Delete LilyPond TimeSignature grob override.
    '''

    note = Note("c'4")
    override(note).time_signature.color = 'red'
    override(note).time_signature.transparent = True
    del(override(note).time_signature)

    assert format(note) == "c'4"
