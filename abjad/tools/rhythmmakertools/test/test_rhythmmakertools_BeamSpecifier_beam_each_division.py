import abjad
from abjad.tools import rhythmmakertools


def test_rhythmmakertools_BeamSpecifier_beam_each_division_01():
    r'''Beam each cell with a multipart beam spanner.
    '''

    talea = rhythmmakertools.Talea(
        counts=[1, 1, 1, -1, 2, 2],
        denominator=32,
        )

    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=[3, 4],
        )

    divisions = [(2, 16), (5, 16)]
    selections = rhythm_maker(divisions)

    maker = abjad.MeasureMaker()
    measures = maker(divisions)
    staff = abjad.Staff(measures)
    abjad.mutate(staff).replace_measure_contents(selections)
    score = abjad.Score([staff])
    abjad.setting(score).autoBeaming = False

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/16
                \times 4/7 {
                    c'32 [
                    c'32
                    c'32 ]
                    r32
                    c'16 [
                    c'32 ~ ]
                }
            } % measure
            { % measure
                \time 5/16
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/7 {
                    c'32 [
                    c'32
                    c'32
                    c'32 ]
                    r32
                    c'16 [
                    c'16
                    c'32
                    c'32
                    c'32 ]
                    r32
                    c'32
                }
            } % measure
        }
        '''
        )
