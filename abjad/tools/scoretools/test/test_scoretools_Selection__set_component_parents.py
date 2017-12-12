import abjad


def test_scoretools_Selection__set_component_parents_01():

    voice_1 = abjad.Voice([])
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")

    selection = voice_2[:]
    selection._set_parents(voice_1)

    assert len(voice_2) == 0

    "Container voice_1 now assigned to selection."
    "But selection not in container voice_1."

    assert selection[0]._parent is voice_1
    assert selection[0] not in voice_1

    voice_1._components.extend(selection)

    "Selection now in container voice_1."

    assert abjad.inspect(voice_1).is_well_formed()
    assert selection[0]._parent is voice_1
    assert selection[0] in voice_1
