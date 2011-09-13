from abjad import *


def test_measuretools_make_measures_with_full_measure_spacer_skips_01():
    '''Make list of skip-populated rigid measures.'''

    t = Staff(measuretools.make_measures_with_full_measure_spacer_skips([(1, 8), (5, 16), (5, 16), (1, 4)]))

    r'''
    \new Staff {
        {
            \time 1/8
            s1 * 1/8
        }
        {
            \time 5/16
            s1 * 5/16
        }
        {
            \time 5/16
            s1 * 5/16
        }
        {
            \time 1/4
            s1 * 1/4
        }
    }
    '''

    assert t.format == '\\new Staff {\n\t{\n\t\t\\time 1/8\n\t\ts1 * 1/8\n\t}\n\t{\n\t\t\\time 5/16\n\t\ts1 * 5/16\n\t}\n\t{\n\t\t\\time 5/16\n\t\ts1 * 5/16\n\t}\n\t{\n\t\t\\time 1/4\n\t\ts1 * 1/4\n\t}\n}'
