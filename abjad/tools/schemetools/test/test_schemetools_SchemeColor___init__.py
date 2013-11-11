# -*- encoding: utf-8 -*-
from abjad import *


def test_schemetools_SchemeColor___init___01():
    r'''Init scheme color with string.
    '''

    note = Note("c'4")
    override(note).note_head.color = schemetools.SchemeColor('ForestGreen')

    assert systemtools.TestManager.compare(
        note,
        r'''
        \once \override NoteHead #'color = #(x11-color 'ForestGreen)
        c'4
        '''
        )


def test_schemetools_SchemeColor___init___02():
    r'''Normal (non-X11) color names specify with a string.
    '''

    note = Note("c'4")
    override(note).note_head.color = 'grey'

    assert systemtools.TestManager.compare(
        note,
        r'''
        \once \override NoteHead #'color = #grey
        c'4
        '''
        )
