import abjad
from abjad import rmakers


def test_TupletRhythmMaker___call___01():
    """
    TupletRhythmMaker can make tuplet monads.
    """


    tuplet_ratios = [(1,)]
    maker = rmakers.TupletRhythmMaker(tuplet_ratios=tuplet_ratios)

    divisions = [(1, 5), (1, 4), (1, 6), (7, 9)]
    result = maker(divisions)
    staff = abjad.Staff(result)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \tweak edge-height #'(0.7 . 0)
            \times 4/5 {
                c'4
            }
            \tweak text #tuplet-number::calc-fraction-text
            \times 1/1 {
                c'4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 8/9 {
                c'2..
            }
        }
        """
        )
