# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_NoteRhythmMaker___call___01():

    maker = rhythmmakertools.NoteRhythmMaker()

    divisions = [(5, 16), (3, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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

    duration_spelling_specifier = rhythmmakertools.DurationSpellingSpecifier(
        decrease_durations_monotonically=False,
        )
    maker = rhythmmakertools.NoteRhythmMaker(
        duration_spelling_specifier=duration_spelling_specifier,
        )

    divisions = [(5, 16), (3, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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
