import abjad
from abjad import rmakers


def test_TaleaRhythmMaker___call___01():

    talea = rmakers.Talea(
        counts=[-1, 4, -2, 3],
        denominator=16,
        )
    rhythm_maker = rmakers.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=[3, 4],
        )

    divisions = [(2, 8), (5, 8)]
    result = rhythm_maker(divisions)

    maker = abjad.MeasureMaker()
    measures = maker(divisions)
    staff = abjad.Staff(measures)
    abjad.mutate(staff).replace_measure_contents(result)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {   % measure
                \time 2/8
                \times 4/7 {
                    r16
                    c'4
                    r8
                }
            }   % measure
            {   % measure
                \time 5/8
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/7 {
                    c'8.
                    r16
                    c'4
                    r8
                    c'8.
                    r16
                }
            }   % measure
        }
        """
        )


def test_TaleaRhythmMaker___call___02():

    talea = rmakers.Talea(
        counts=[-1, 4, -2, 3],
        denominator=16,
        )
    rhythm_maker = rmakers.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=[3, 4],
        split_divisions_by_counts=[6],
        )

    divisions = [(2, 8), (5, 8)]
    result = rhythm_maker(divisions)

    maker = abjad.MeasureMaker()
    measures = maker(divisions)
    staff = abjad.Staff(measures)
    abjad.mutate(staff).replace_measure_contents(result)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {   % measure
                \time 2/8
                \times 4/7 {
                    r16
                    c'4
                    r8
                }
            }   % measure
            {   % measure
                \time 5/8
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8
                    ~
                }
                \times 2/3 {
                    c'16
                    r16
                    c'4
                    r8
                    c'16
                    ~
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8
                }
            }   % measure
        }
        """
        )
