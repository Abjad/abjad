import abjad
from abjad import rhythmos


def test_rhythmos_TieSpecifier_01():

    divisions = [(3, 8), (5, 16), (1, 4), (5, 16)]
    rhythm_maker = rhythmos.TaleaRhythmMaker(
        burnish_specifier=rhythmos.BurnishSpecifier(
            left_classes=[abjad.Rest, abjad.Note],
            left_counts=[1],
            ),
        extra_counts_per_division=[0, 1, 1],
        talea=rhythmos.Talea(
            counts=[1, 2, 3],
            denominator=16,
            ),
        tie_specifier=rhythmos.TieSpecifier(
            tie_across_divisions=True,
            ),
        )
    selections = rhythm_maker(divisions)
    staff = abjad.Staff(selections)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \tweak text #tuplet-number::calc-fraction-text
            \times 1/1 {
                r16
                c'8
                [
                c'8.
                ~
                ]
            }
            \tweak text #tuplet-number::calc-fraction-text
            \times 5/6 {
                c'16
                [
                c'8
                c'8.
                ]
            }
            \times 4/5 {
                r16
                c'8
                [
                c'8
                ~
                ]
            }
            \tweak text #tuplet-number::calc-fraction-text
            \times 1/1 {
                c'16
                [
                c'16
                c'8
                c'16
                ]
            }
        }
        """
        )
