from abjad import *
from abjad.tools import durtools


def test_durtools_duration_pair_to_prolation_string_01():

    assert durtools.duration_pair_to_prolation_string((1, 1)) == '1:1'
    assert durtools.duration_pair_to_prolation_string((1, 2)) == '2:1'
    assert durtools.duration_pair_to_prolation_string((2, 2)) == '2:2'
    assert durtools.duration_pair_to_prolation_string((1, 3)) == '3:1'
    assert durtools.duration_pair_to_prolation_string((2, 3)) == '3:2'
    assert durtools.duration_pair_to_prolation_string((3, 3)) == '3:3'
    assert durtools.duration_pair_to_prolation_string((1, 4)) == '4:1'
    assert durtools.duration_pair_to_prolation_string((2, 4)) == '4:2'
    assert durtools.duration_pair_to_prolation_string((3, 4)) == '4:3'
    assert durtools.duration_pair_to_prolation_string((4, 4)) == '4:4'

