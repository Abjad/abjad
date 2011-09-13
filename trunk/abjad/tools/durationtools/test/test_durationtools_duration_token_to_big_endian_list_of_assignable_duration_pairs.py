from abjad import *
from abjad.tools import durationtools


def test_durationtools_duration_token_to_big_endian_list_of_assignable_duration_pairs_01():
    '''Return big-endian list of note_head-assignable duration tokens.'''

    assert durationtools.duration_token_to_big_endian_list_of_assignable_duration_pairs((10, 16)) == ((8, 16), (2, 16))
    assert durationtools.duration_token_to_big_endian_list_of_assignable_duration_pairs((11, 16)) == ((8, 16), (3, 16))
    assert durationtools.duration_token_to_big_endian_list_of_assignable_duration_pairs((12, 16)) == ((12, 16), )
    assert durationtools.duration_token_to_big_endian_list_of_assignable_duration_pairs((13, 16)) == ((12, 16), (1, 16))
    assert durationtools.duration_token_to_big_endian_list_of_assignable_duration_pairs((14, 16)) == ((14, 16), )
    assert durationtools.duration_token_to_big_endian_list_of_assignable_duration_pairs((15, 16)) == ((15, 16), )
    assert durationtools.duration_token_to_big_endian_list_of_assignable_duration_pairs((16, 16)) == ((16, 16), )
    assert durationtools.duration_token_to_big_endian_list_of_assignable_duration_pairs((17, 16)) == ((16, 16), (1, 16))
    assert durationtools.duration_token_to_big_endian_list_of_assignable_duration_pairs((18, 16)) == ((16, 16), (2, 16))
    assert durationtools.duration_token_to_big_endian_list_of_assignable_duration_pairs((19, 16)) == ((16, 16), (3, 16))
