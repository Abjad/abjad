from abjad import *


def test_tietools_iterate_topmost_tie_chains_and_components_forward_in_expr_01():
    '''Iterate toplevel contents with tie chains in place of leaves.'''

    t = Staff(notetools.make_notes(0, [(5, 32)] * 4))
    t.insert(4, tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)))
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Staff {
        c'8 ~
        c'32
        \times 2/3 {
            d'8
            e'8
            f'8
        }
        g'8 ~
        g'32
        a'8 ~
        a'32
        b'8 ~
        b'32
    }
    '''

    chained_contents = list(tietools.iterate_topmost_tie_chains_and_components_forward_in_expr(t))

    assert chained_contents[0] == tietools.get_tie_chain(t[0])
    assert chained_contents[1] == tietools.get_tie_chain(t[2])
    assert chained_contents[2] is t[4]
    assert chained_contents[3] == tietools.get_tie_chain(t[5])
    assert chained_contents[4] == tietools.get_tie_chain(t[7])
