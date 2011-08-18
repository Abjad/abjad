from abjad import *


def test_voicetools_get_first_voice_in_proper_parentage_of_component_01():

    voice = Voice("c'8 d'8 e'8 f'8")
    staff = Staff([voice])

    assert voicetools.get_first_voice_in_proper_parentage_of_component(staff.leaves[0]) is voice
    assert voicetools.get_first_voice_in_proper_parentage_of_component(staff.leaves[1]) is voice
    assert voicetools.get_first_voice_in_proper_parentage_of_component(staff.leaves[2]) is voice
    assert voicetools.get_first_voice_in_proper_parentage_of_component(staff.leaves[3]) is voice

    assert voicetools.get_first_voice_in_proper_parentage_of_component(voice) is None
    assert voicetools.get_first_voice_in_proper_parentage_of_component(staff) is None
