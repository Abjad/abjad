from abjad import *
from abjad.tools import sequencetools
from abjad.tools import timetokentools


def test_RestFilleTimeTokenMaker___call___01():

    maker = timetokentools.RestFilledTimeTokenMaker()

    duration_tokens = [(5, 16), (3, 8)]
    leaf_lists = maker(duration_tokens)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
    measuretools.replace_contents_of_measures_in_expr(staff, leaves)

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

    assert staff.lilypond_format == '\\new Staff {\n\t{\n\t\t\\time 5/16\n\t\tr4\n\t\tr16\n\t}\n\t{\n\t\t\\time 3/8\n\t\tr4.\n\t}\n}'
