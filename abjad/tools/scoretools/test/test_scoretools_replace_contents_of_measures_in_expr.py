# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_replace_contents_of_measures_in_expr_01():
    r'''Contents duration less than sum of duration of measures.
    Note spacer skip at end of second measure.
    '''

    staff = Staff(scoretools.make_measures_with_full_measure_spacer_skips([(1, 8), (3, 16)]))

    r'''
    \new Staff {
        {
            \time 1/8
            s1 * 1/8
        }
        {
            \time 3/16
            s1 * 3/16
        }
    }
    '''

    notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16")]
    scoretools.replace_contents_of_measures_in_expr(staff, notes)

    r'''
    \new Staff {
        {
            \time 1/8
            c'16
            d'16
        }
        {
            \time 3/16
            e'16
            f'16
            s1 * 1/16
        }
    }
    '''

    assert inspect(staff).is_well_formed()
    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/8
                c'16
                d'16
            }
            {
                \time 3/16
                e'16
                f'16
                s1 * 1/16
            }
        }
        '''
        )


def test_scoretools_replace_contents_of_measures_in_expr_02():
    r'''Some contents too big for some measures.
    Small measures skipped.
    '''

    staff = Staff(scoretools.make_measures_with_full_measure_spacer_skips([(1, 16), (3, 16), (1, 16), (3, 16)]))

    r'''
    \new Staff {
        {
            \time 1/16
            s1 * 1/16
        }
        {
            \time 3/16
            s1 * 3/16
        }
        {
            \time 1/16
            s1 * 1/16
        }
        {
            \time 3/16
            s1 * 3/16
        }
    }
    '''

    notes = [Note("c'8"), Note("d'8")]
    scoretools.replace_contents_of_measures_in_expr(staff, notes)

    r'''
    \new Staff {
        {
            \time 1/16
            s1 * 1/16
        }
        {
            \time 3/16
            c'8
            s1 * 1/16
        }
        {
            \time 1/16
            s1 * 1/16
        }
        {
            \time 3/16
            d'8
            s1 * 1/16
        }
    }
    '''

    assert inspect(staff).is_well_formed()
    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/16
                s1 * 1/16
            }
            {
                \time 3/16
                c'8
                s1 * 1/16
            }
            {
                \time 1/16
                s1 * 1/16
            }
            {
                \time 3/16
                d'8
                s1 * 1/16
            }
        }
        '''
        )


def test_scoretools_replace_contents_of_measures_in_expr_03():
    r'''Raise MissingMeasureError when input expression
    contains no measures.
    '''

    note = Note("c'4")
    notes = [Note("c'8"), Note("d'8")]

    assert pytest.raises(MissingMeasureError, 'scoretools.replace_contents_of_measures_in_expr(note, notes)')


def test_scoretools_replace_contents_of_measures_in_expr_04():
    r'''Raise StopIteration when not enough measures.
    '''

    staff = Staff(scoretools.make_measures_with_full_measure_spacer_skips([(1, 8), (1, 8)]))
    notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16"), Note("g'16"), Note("a'16")]

    assert pytest.raises(StopIteration,
        'scoretools.replace_contents_of_measures_in_expr(staff, notes)')


def test_scoretools_replace_contents_of_measures_in_expr_05():
    r'''Populate measures even when not enough total measures.
    '''

    staff = Staff(scoretools.make_measures_with_full_measure_spacer_skips([(1, 8), (1, 8)]))
    scoretools.set_always_format_time_signature_of_measures_in_expr(staff)
    notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16"), Note("g'16"), Note("a'16")]

    try:
        scoretools.replace_contents_of_measures_in_expr(staff, notes)
    except StopIteration:
        pass

    r'''
    \new Staff {
        {
            \time 1/8
            c'16
            d'16
        }
        {
            \time 1/8
            e'16
            f'16
        }
    }
    '''

    assert inspect(staff).is_well_formed()
    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/8
                c'16
                d'16
            }
            {
                \time 1/8
                e'16
                f'16
            }
        }
        '''
        )


def test_scoretools_replace_contents_of_measures_in_expr_06():
    r'''Preserve ties.
    '''

    maker = rhythmmakertools.NoteRhythmMaker()
    durations = [(5, 16), (3, 16)]
    leaf_lists = maker(durations)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_measures_with_full_measure_spacer_skips(
        durations)
    staff = Staff(measures)
    measures = scoretools.replace_contents_of_measures_in_expr(staff, leaves)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 5/16
                c'4 ~
                c'16
            }
            {
                \time 3/16
                c'8.
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
