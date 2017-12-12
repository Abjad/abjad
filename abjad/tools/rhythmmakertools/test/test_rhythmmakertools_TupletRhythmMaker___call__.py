import abjad
from abjad.tools import rhythmmakertools


def test_rhythmmakertools_TupletRhythmMaker___call___01():
    r'''TupletRhythmMaker can make tuplet monads.
    '''


    tuplet_ratios = [(1,)]
    maker = rhythmmakertools.TupletRhythmMaker(tuplet_ratios=tuplet_ratios)

    divisions = [(1, 5), (1, 4), (1, 6), (7, 9)]
    result = maker(divisions)
    staff = abjad.Staff(result)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \tweak edge-height #'(0.7 . 0)
            \times 4/5 {
                c'4
            }
            {
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
        '''
        )
