from abjad import *


def test_tietools_add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration_01():
    '''Scale trivial tie chain to nontrivial tie chain.'''

    t = Staff(notetools.make_repeated_notes(1))
    spannertools.BeamSpanner(t[:])
    tietools.add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration(
        tietools.get_tie_chain(t[0]), Duration(5, 4))

    r'''
    \new Staff {
        c'8 [ ~
        c'32 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 [ ~\n\tc'32 ]\n}"


def test_tietools_add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration_02():
    '''Scale nontrivial tie chain to trivial tie chain.'''

    t = Staff(notetools.make_notes(0, [(5, 32)]))
    spannertools.BeamSpanner(t[:])
    tietools.add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration(
        tietools.get_tie_chain(t[0]), Duration(4, 5))

    r'''
    \new Staff {
        c'8 [ ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 [ ]\n}"
