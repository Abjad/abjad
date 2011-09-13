from abjad import *


def test_tietools_remove_all_leaves_in_tie_chain_except_first_01():
    '''Keep and unspan first note in tie chain only.'''

    t = Staff(notetools.make_notes(0, [(5, 16)]))

    r'''
    \new Staff {
        c'4 ~
        c'16
    }
    '''

    tietools.remove_all_leaves_in_tie_chain_except_first(tietools.get_tie_chain(t[0]))

    r'''
    \new Staff {
        c'4
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'4\n}"


def test_tietools_remove_all_leaves_in_tie_chain_except_first_02():
    '''No effect on length-1 tie chains.'''

    t = Staff(notetools.make_repeated_notes(1))

    tietools.remove_all_leaves_in_tie_chain_except_first(tietools.get_tie_chain(t[0]))

    r'''
    \new Staff {
        c'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8\n}"
