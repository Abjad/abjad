import abjad
from abjad.tools import rhythmmakertools


def test_rhythmmakertools_NoteRhythmMaker___call___01():

    maker = rhythmmakertools.NoteRhythmMaker()

    divisions = [(5, 16), (3, 8)]
    leaf_lists = maker(divisions)
    leaves = abjad.sequence(leaf_lists).flatten()

    maker = abjad.MeasureMaker()
    measures = maker(divisions)
    staff = abjad.Staff(measures)
    abjad.mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == abjad.String.normalize(
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

    duration_specifier = rhythmmakertools.DurationSpecifier(
        decrease_monotonic=False,
        )
    maker = rhythmmakertools.NoteRhythmMaker(
        duration_specifier=duration_specifier,
        )

    divisions = [(5, 16), (3, 8)]
    leaf_lists = maker(divisions)
    leaves = abjad.sequence(leaf_lists).flatten()

    maker = abjad.MeasureMaker()
    measures = maker(divisions)
    staff = abjad.Staff(measures)
    abjad.mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == abjad.String.normalize(
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
