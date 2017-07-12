# -*- coding: utf-8 -*-
import abjad


def test_schemetools_SchemeColor___init___01():
    r'''Initialize scheme color with string.
    '''

    note = abjad.Note("c'4")
    abjad.override(note).note_head.color = abjad.SchemeColor('ForestGreen')

    assert format(note) == abjad.String.normalize(
        r'''
        \once \override NoteHead.color = #(x11-color 'ForestGreen)
        c'4
        '''
        )


def test_schemetools_SchemeColor___init___02():
    r'''Normal (non-X11) color names specify with a string.
    '''

    note = abjad.Note("c'4")
    abjad.override(note).note_head.color = 'grey'

    assert format(note) == abjad.String.normalize(
        r'''
        \once \override NoteHead.color = #grey
        c'4
        '''
        )
