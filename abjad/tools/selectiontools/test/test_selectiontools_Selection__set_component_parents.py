# -*- coding: utf-8 -*-
import abjad


def test_selectiontools_Selection__set_component_parents_01():

    voice = abjad.Voice([])
    u = abjad.Voice("c'8 d'8 e'8 f'8")

    selection = u[:]
    selection._set_parents(voice)

    assert len(u) == 0

    "Container voice now assigned to selection."
    "But selection not in container voice."

    assert selection[0]._parent is voice
    assert selection[0] not in voice

    voice._music.extend(selection)

    "Selection now in container voice."

    assert abjad.inspect(voice).is_well_formed()
    assert selection[0]._parent is voice
    assert selection[0] in voice