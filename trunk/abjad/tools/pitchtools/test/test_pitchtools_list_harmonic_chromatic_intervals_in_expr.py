from abjad import *


def test_pitchtools_list_harmonic_chromatic_intervals_in_expr_01():

    staff = Staff("c'8 d'8 e'8 f'8")

    intervals = pitchtools.list_harmonic_chromatic_intervals_in_expr(staff)
    intervals = sorted(list(intervals))
    numbers = [hci.number for hci in intervals]

    assert numbers == [1, 2, 2, 3, 4, 5]
