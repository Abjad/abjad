# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_LogicalTie__add_or_remove_notes_to_achieve_written_duration_01():
    r'''Change trivial logical tie to nontrivial logical tie.
    '''

    staff = Staff("c'8 [ ]")
    logical_tie = inspect_(staff[0]).get_logical_tie()
    logical_tie._add_or_remove_notes_to_achieve_written_duration(Duration(5, 32))

    r'''
    \new Staff {
        c'8 ~ [
        c'32 ]
    }
    '''

    assert inspect_(staff).is_well_formed()
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 ~ [
            c'32 ]
        }
        '''
        )


def test_selectiontools_LogicalTie__add_or_remove_notes_to_achieve_written_duration_02():
    r'''Change nontrivial logical tie to trivial logical tie.
    '''

    staff = Staff("c'8 ~ [ c'32 ]")
    logical_tie = inspect_(staff[0]).get_logical_tie()
    logical_tie._add_or_remove_notes_to_achieve_written_duration(Duration(1, 8))

    r'''
    \new Staff {
        c'8 [ ]
    }
    '''

    assert inspect_(staff).is_well_formed()
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [ ]
        }
        '''
        )
