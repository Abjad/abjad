# -*- encoding: utf-8 -*-
from abjad import *


def test_SchemeColor___init___01():
    r'''Init scheme color with string.
    '''

    t = Note("c'4")
    t.override.note_head.color = schemetools.SchemeColor('ForestGreen')

    r'''
    \once \override NoteHead #'color = #(x11-color 'ForestGreen)
    c'4
    '''

    assert testtools.compare(
        t.lilypond_format,
        r'''
        \once \override NoteHead #'color = #(x11-color 'ForestGreen)
        c'4
        '''
        )


def test_SchemeColor___init___02():
    r'''Normal (non-X11) color names specify with a string.
    '''

    t = Note("c'4")
    t.override.note_head.color = 'grey'

    r'''
    \once \override NoteHead #'color = #grey
    c'4
    '''

    assert testtools.compare(
        t.lilypond_format,
        r'''
        \once \override NoteHead #'color = #grey
        c'4
        '''
        )
