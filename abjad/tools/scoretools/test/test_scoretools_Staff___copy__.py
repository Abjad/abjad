# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_scoretools_Staff___copy___01():
    r'''Staves (shallow) copy grob overrides and context settings
    but not musical content.
    '''

    staff_1 = Staff("c'8 d'8 e'8 f'8")
    override(staff_1).note_head.color = 'red'
    set_(staff_1).tuplet_full_length = True


    staff_2 = copy.copy(staff_1)

    assert format(staff_2) == stringtools.normalize(
        r'''
        \new Staff \with {
            \override NoteHead.color = #red
            tupletFullLength = ##t
        } {
        }
        '''
        )
