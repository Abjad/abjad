from abjad import *
from abjad.tools.componenttools._set_component_parents_to_none \
	import _set_component_parents_to_none
from abjad.tools.componenttools._restore_component_parents \
	import _restore_component_parents


def test_componenttools__restore_component_parents_01():

    t = Voice("c'8 d'8 e'8 f'8")
    beamtools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    receipt = _set_component_parents_to_none(t[:])

    assert not wellformednesstools.is_well_formed_component(t)

    _restore_component_parents(receipt)

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
