# -*- encoding: utf-8 -*-
from abjad import *


def test_ComponentSelection_detach_marks_01():
    r'''Detach tie spanners.
    '''

    staff = Staff(notetools.make_notes(0, [(5, 16), (5, 16)]))

    r'''
    \new Staff {
        c'4 ~
        c'16
        c'4 ~
        c'16
    }
    '''

    spanner_classes = (spannertools.TieSpanner,)
    select(staff).detach_spanners(spanner_classes=spanner_classes)

    r'''
    \new Staff {
        c'4
        c'16
        c'4
        c'16
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'4
            c'16
            c'4
            c'16
        }
        '''
        )


def test_ComponentSelection_detach_marks_02():
    r'''Handles empty selection without exception.
    '''

    select().detach_spanners()
