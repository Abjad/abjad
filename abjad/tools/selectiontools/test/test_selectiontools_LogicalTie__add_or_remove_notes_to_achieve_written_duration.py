# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_LogicalTie__add_or_remove_notes_to_achieve_written_duration_01():
    r'''Change trivial tie chain to nontrivial tie chain.
    '''

    staff = Staff("c'8 [ ]")
    tie_chain = inspect(staff[0]).get_tie_chain()
    tie_chain._add_or_remove_notes_to_achieve_written_duration(Duration(5, 32))

    r'''
    \new Staff {
        c'8 [ ~
        c'32 ]
    }
    '''

    assert inspect(staff).is_well_formed()
    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ ~
            c'32 ]
        }
        '''
        )


def test_selectiontools_LogicalTie__add_or_remove_notes_to_achieve_written_duration_02():
    r'''Change nontrivial tie chain to trivial tie chain.
    '''

    staff = Staff("c'8 [ ~ c'32 ]")
    tie_chain = inspect(staff[0]).get_tie_chain()
    tie_chain._add_or_remove_notes_to_achieve_written_duration(Duration(1, 8))

    r'''
    \new Staff {
        c'8 [ ]
    }
    '''

    assert inspect(staff).is_well_formed()
    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ ]
        }
        '''
        )
