import abjad
from abjad.tools import rhythmmakertools


def test_rhythmmakertools_TaleaRhythmMaker_tie_split_notes_01():

    talea = rhythmmakertools.Talea(
        counts=[5],
        denominator=16,
        )
    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        )

    divisions = [(2, 8), (2, 8), (2, 8), (2, 8)]
    result = rhythm_maker(divisions)

    maker = abjad.MeasureMaker()
    measures = maker(divisions)
    staff = abjad.Staff(measures)
    measures = abjad.mutate(staff).replace_measure_contents(result)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'4 ~
            } % measure
            { % measure
                c'16 [
                c'8. ~ ]
            } % measure
            { % measure
                c'8 [
                c'8 ~ ]
            } % measure
            { % measure
                c'8. [
                c'16 ]
            } % measure
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_rhythmmakertools_TaleaRhythmMaker_tie_split_notes_02():

    talea = rhythmmakertools.Talea(
        counts=[5],
        denominator=16,
        )
    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        )

    divisions = [(3, 16), (5, 8), (4, 8), (7, 16)]
    result = rhythm_maker(divisions)

    maker = abjad.MeasureMaker()
    measures = maker(divisions)
    staff = abjad.Staff(measures)
    measures = abjad.mutate(staff).replace_measure_contents(result)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 3/16
                c'8. ~
            } % measure
            { % measure
                \time 5/8
                c'8
                c'4 ~
                c'16 [
                c'8. ~ ]
            } % measure
            { % measure
                \time 4/8
                c'8
                c'4 ~
                c'16 [
                c'16 ~ ]
            } % measure
            { % measure
                \time 7/16
                c'4
                c'8.
            } % measure
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
