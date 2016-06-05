# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_agenttools_MutationAgent_replace_measure_contents_01():
    r'''Contents duration less than sum of duration of measures.
    Note spacer skip at end of second measure.
    '''

    measures = scoretools.make_spacer_skip_measures([(1, 8), (3, 16)])
    staff = Staff(measures)
    notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16")]
    mutate(staff).replace_measure_contents(notes)

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_replace_measure_contents_02():
    r'''Some contents too big for some measures.
    Small measures skipped.
    '''

    time_signatures = [(1, 16), (3, 16), (1, 16), (3, 16)]
    measures = scoretools.make_spacer_skip_measures(time_signatures)
    staff = Staff(measures)
    notes = [Note("c'8"), Note("d'8")]
    mutate(staff).replace_measure_contents(notes)

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_replace_measure_contents_03():
    r'''Raise MissingMeasureError when input expression
    contains no measures.
    '''

    note = Note("c'4")
    notes = [Note("c'8"), Note("d'8")]
    statement = 'mutate(note).replace_measure_contents(notes)'
    assert pytest.raises(MissingMeasureError, statement)


def test_agenttools_MutationAgent_replace_measure_contents_04():
    r'''Raise StopIteration when not enough measures.
    '''

    measures = scoretools.make_spacer_skip_measures([(1, 8), (1, 8)])
    staff = Staff(measures)
    notes = [Note("c'16"), Note("d'16"), Note("e'16"),
        Note("f'16"), Note("g'16"), Note("a'16")]
    statement = 'mutate(staff).replace_measure_contents(notes)'
    assert pytest.raises(StopIteration, statement)


def test_agenttools_MutationAgent_replace_measure_contents_05():
    r'''Populate measures even when not enough total measures.
    '''

    measures = scoretools.make_spacer_skip_measures([(1, 8), (1, 8)])
    staff = Staff(measures)
    notes = [Note("c'16"), Note("d'16"), Note("e'16"),
        Note("f'16"), Note("g'16"), Note("a'16")]

    try:
        mutate(staff).replace_measure_contents(notes)
    except StopIteration:
        pass

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 1/8
                c'16
                d'16
            }
            {
                e'16
                f'16
            }
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_replace_measure_contents_06():
    r'''Preserve ties.
    '''

    maker = rhythmmakertools.NoteRhythmMaker()
    durations = [(5, 16), (3, 16)]
    leaf_lists = maker(durations)
    leaves = sequencetools.flatten_sequence(leaf_lists)
    measures = scoretools.make_spacer_skip_measures(durations)
    staff = Staff(measures)
    measures = mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()
