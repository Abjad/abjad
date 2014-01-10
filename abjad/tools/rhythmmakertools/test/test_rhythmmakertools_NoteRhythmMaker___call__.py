# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_NoteRhythmMaker___call___01():

    maker = rhythmmakertools.NoteRhythmMaker()

    divisions = [(5, 16), (3, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

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
                \time 3/8
                c'4.
            }
        }
        '''
        )


def test_rhythmmakertools_NoteRhythmMaker___call___02():

    maker = rhythmmakertools.NoteRhythmMaker(
        decrease_durations_monotonically=False,
        )

    divisions = [(5, 16), (3, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 5/16
                c'16 ~
                c'4
            }
            {
                \time 3/8
                c'4.
            }
        }
        '''
        )
