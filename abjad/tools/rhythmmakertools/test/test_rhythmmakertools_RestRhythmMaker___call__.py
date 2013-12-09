# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools
from abjad.tools import rhythmmakertools


def test_rhythmmakertools_RestRhythmMaker___call___01():

    maker = rhythmmakertools.RestRhythmMaker()

    divisions = [(5, 16), (3, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(scoretools.make_spacer_skip_measures(divisions))
    scoretools.replace_contents_of_measures_in_expr(staff, leaves)

    r'''
    \new Staff {
        {
            \time 5/16
            r4
            r16
        }
        {
            \time 3/8
            r4.
        }
    }
    '''

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 5/16
                r4
                r16
            }
            {
                \time 3/8
                r4.
            }
        }
        '''
        )
