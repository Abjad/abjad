# -*- encoding: utf-8 -*-
from abjad import *


def test_FreeTupletSelection_remove_01():

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    assert len(staff) == 2

    r'''
    \new Staff {
            c'8
            d'8
            e'8
            f'8
    }
    '''

    tuplets = selectiontools.select_tuplets(
        staff,
        include_augmented_tuplets=False,
        include_diminished_tuplets=False,
        )
    tuplets.remove()

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert inspect(staff).is_well_formed()
    assert len(staff) == 4
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )
