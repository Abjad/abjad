from abjad import *
from abjad.tools.componenttools._set_component_parents \
	import _set_component_parents


def test_componenttools__set_component_parents_01():

    t = Voice([])
    u = Voice("c'8 d'8 e'8 f'8")

    components = u[:]
    _set_component_parents(components, t)

    assert wellformednesstools.is_well_formed_component(u)
    assert len(u) == 0

    "Container t now assigned to components."
    "But components not in container t."

    assert components[0]._parent is t
    assert components[0] not in t

    t._music.extend(components)

    "Components now in container t."

    assert wellformednesstools.is_well_formed_component(t)
    assert components[0]._parent is t
    assert components[0] in t
