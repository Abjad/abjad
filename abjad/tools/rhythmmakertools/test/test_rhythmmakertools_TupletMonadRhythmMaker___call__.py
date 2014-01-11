# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_TupletMonadRhythmMaker___call___01():

    maker = rhythmmakertools.TupletMonadRhythmMaker()

    divisions = [(1, 5), (1, 4), (1, 6), (7, 9)]
    tuplet_lists = maker(divisions)
    tuplets = sequencetools.flatten_sequence(tuplet_lists)
    staff = Staff(tuplets)

    r'''
    \new Staff {
        \times 4/5 {
            c'4
        }
        {
            c'4
        }
        \times 2/3 {
            c'4
        }
        \times 8/9 {
            c'2..
        }
    }
    '''

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            \times 4/5 {
                c'4
            }
            {
                c'4
            }
            \times 2/3 {
                c'4
            }
            \times 8/9 {
                c'2..
            }
        }
        '''
        )
