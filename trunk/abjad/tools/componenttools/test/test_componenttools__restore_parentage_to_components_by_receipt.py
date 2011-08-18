from abjad import *
from abjad.tools.componenttools._ignore_parentage_of_components import _ignore_parentage_of_components
from abjad.tools.componenttools._restore_parentage_to_components_by_receipt import _restore_parentage_to_components_by_receipt


def test_componenttools__restore_parentage_to_components_by_receipt_01():

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    receipt = _ignore_parentage_of_components(t[:])

    assert not componenttools.is_well_formed_component(t)

    _restore_parentage_to_components_by_receipt(receipt)

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
