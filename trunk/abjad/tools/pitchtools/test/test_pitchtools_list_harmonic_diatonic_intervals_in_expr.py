from abjad import *


def test_pitchtools_list_harmonic_diatonic_intervals_in_expr_01():

    staff = Staff("c'8 d'8 e'8 f'8")

    intervals = pitchtools.list_harmonic_diatonic_intervals_in_expr(staff)
    intervals = list(intervals)
    numbers = [hdi.number for hdi in intervals]
    numbers.sort()

    assert numbers == [2, 2, 2, 3, 3, 4]
