import abjad
import copy


def test_spannertools_Beam___copy___01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    beam_1 = abjad.Beam()
    abjad.attach(beam_1, staff[:])
    beam_2 = copy.copy(beam_1)

    assert beam_1 is not beam_2
    assert len(beam_1) == 4
    assert len(beam_2) == 0
