from abjad import *
import copy


def test_BeamSpanner___copy___01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beam_1 = spannertools.BeamSpanner(staff[:])
    beam_2 = copy.copy(beam_1)

    assert beam_1 is not beam_2
    assert len(beam_1) == 4
    assert len(beam_2) == 0
