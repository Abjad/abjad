from abjad import *


def test_skiptools_make_skips_with_multiplied_durations_01():

    durations = [(1, 2), (1, 3), (1, 4), (1, 5)]
    durations = [Duration(*x) for x in durations]
    staff = Staff(skiptools.make_skips_with_multiplied_durations(Duration(1, 4), durations))

    r'''
    \new Staff {
        s4 * 2
        s4 * 4/3
        s4 * 1
        s4 * 4/5
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == '\\new Staff {\n\ts4 * 2\n\ts4 * 4/3\n\ts4 * 1\n\ts4 * 4/5\n}'
