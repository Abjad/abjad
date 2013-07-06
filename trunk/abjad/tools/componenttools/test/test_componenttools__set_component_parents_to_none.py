from abjad import *
from abjad.tools.componenttools._sever_component_parents \
	import _sever_component_parents


def test_componenttools__sever_component_parents_01():

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

    receipt = _sever_component_parents(t[:])

    assert not wellformednesstools.is_well_formed_component(t)

    assert (t[0], t) in receipt
    assert (t[1], t) in receipt
    assert (t[2], t) in receipt
    assert (t[3], t) in receipt

    "Follow soon after with componenttools.restore(receipt)."
