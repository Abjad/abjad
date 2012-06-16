from abjad import *


def test_tietools_add_or_remove_tie_chain_notes_to_achieve_written_duration_01():
    '''Change trivial tie chain to nontrivial tie chain.
    '''

    staff = Staff("c'8 [ ]")
    tie_chain = tietools.get_tie_chain(staff[0])
    tietools.add_or_remove_tie_chain_notes_to_achieve_written_duration(tie_chain, Duration(5, 32))

    r'''
    \new Staff {
        c'8 [ ~
        c'32 ]
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [ ~\n\tc'32 ]\n}"


def test_tietools_add_or_remove_tie_chain_notes_to_achieve_written_duration_02():
    '''Change nontrivial tie chain to trivial tie chain.
    '''

    staff = Staff("c'8 [ ~ c'32 ]")
    tie_chain = tietools.get_tie_chain(staff[0])
    tietools.add_or_remove_tie_chain_notes_to_achieve_written_duration(tie_chain, Duration(1, 8))

    r'''
    \new Staff {
        c'8 [ ]
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [ ]\n}"
