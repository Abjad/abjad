# -*- encoding: utf-8 -*-
import copy
from abjad import *


def test_scoretools_Staff___copy___01():
    r'''Staves (shallow) copy grob overrides and context settings 
    but not musical content.
    '''

    staff_1 = Staff("c'8 d'8 e'8 f'8")
    override(staff_1).note_head.color = 'red'
    staff_1.set.tuplet_full_length = True


    staff_2 = copy.copy(staff_1)

    assert testtools.compare(
        staff_2,
        r'''
        \new Staff \with {
            \override NoteHead #'color = #red
            tupletFullLength = ##t
        } {
        }
        '''
        )
