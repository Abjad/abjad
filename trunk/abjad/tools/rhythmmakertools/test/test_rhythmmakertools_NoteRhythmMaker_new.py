# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_NoteRhythmMaker_new_01():

    maker = rhythmmakertools.NoteRhythmMaker()

    divisions = [(5, 16), (3, 8)]
    leaf_lists = maker.new(decrease_durations_monotonically=False)(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
    measuretools.replace_contents_of_measures_in_expr(staff, leaves)

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

    assert testtools.compare(
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
