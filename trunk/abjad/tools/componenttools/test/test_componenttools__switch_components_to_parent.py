from abjad import *
from abjad.tools.componenttools._switch_components_to_parent import _switch_components_to_parent


def test_componenttools__switch_components_to_parent_01():

    t = Voice([])
    u = Voice("c'8 d'8 e'8 f'8")

    components = u[:]
    _switch_components_to_parent(components, t)

    assert componenttools.is_well_formed_component(u)
    assert len(u) == 0

    "Container t now assigned to components."
    "But components not in container t."

    assert components[0]._parentage.parent is t
    assert components[0] not in t

    t._music.extend(components)

    "Components now in container t."

    assert componenttools.is_well_formed_component(t)
    assert components[0]._parentage.parent is t
    assert components[0] in t
