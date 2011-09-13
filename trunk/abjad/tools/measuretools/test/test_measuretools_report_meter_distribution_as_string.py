from abjad import *


def test_measuretools_report_meter_distribution_as_string_01():

    meters = [(1, 8), (3, 16), (5, 16), (5, 16)]
    t = Staff(measuretools.make_measures_with_full_measure_spacer_skips(meters))

    r'''
    \new Staff {
        {
            \time 1/8
            s1 * 1/8
        }
        {
            \time 3/16
            s1 * 3/16
        }
        {
            \time 5/16
            s1 * 5/16
        }
        {
            \time 5/16
            s1 * 5/16
        }
    }
    '''

    report = measuretools.report_meter_distribution_as_string(t)

    r'''
        1/8     1
        3/16    1
        5/16    2
    '''

    assert report == '\t1/8\t1\n\t3/16\t1\n\t5/16\t2\n'
