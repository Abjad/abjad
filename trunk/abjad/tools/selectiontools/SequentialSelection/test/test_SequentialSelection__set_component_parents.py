from abjad import *


def test_SequentialSelection__set_component_parents_01():

    t = Voice([])
    u = Voice("c'8 d'8 e'8 f'8")

    selection = u[:]
    selection._set_parents(t)

    assert inspect(u).is_well_formed()
    assert len(u) == 0

    "Container t now assigned to selection."
    "But selection not in container t."

    assert selection[0]._parent is t
    assert selection[0] not in t

    t._music.extend(selection)

    "SequentialSelection now in container t."

    assert inspect(t).is_well_formed()
    assert selection[0]._parent is t
    assert selection[0] in t
