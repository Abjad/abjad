# -*- encoding: utf-8 -*-
from abjad import *


def test_FreeTupletSelection_move_prolation_to_contents_and_remove_01():
    r'''Scale tuplet contents and then bequeath in-score position
    of tuplet to contents.
    '''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(3, 8), "c'8 d'8") * 2)
    spannertools.BeamSpanner(t.select_leaves())

    r'''
    \new Staff {
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'8 [
            d'8
        }
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'8
            d'8 ]
        }
    }
    '''

    selection = selectiontools.select_tuplets(t[0])
    selection.move_prolation_to_contents_and_remove()

    r'''
    \new Staff {
        c'8. [
        d'8.
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'8
            d'8 ]
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            c'8. [
            d'8.
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/2 {
                c'8
                d'8 ]
            }
        }
        '''
        )


def test_FreeTupletSelection_move_prolation_to_contents_and_remove_02():
    r'''Scale tuplet contents and then bequeath in-score position
    of tuplet to contents.
    '''

    t = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Voice {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    selection = selectiontools.select_tuplets(t[0])
    selection.move_prolation_to_contents_and_remove()

    r'''
    \new Voice {
        \times 2/3 {
            c'8
        }
        \times 2/3 {
            d'8
        }
        \times 2/3 {
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            \times 2/3 {
                c'8
            }
            \times 2/3 {
                d'8
            }
            \times 2/3 {
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8
            }
        }
        '''
        )
