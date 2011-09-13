from abjad import *


def test_DynamicMeasure_suppress_meter_01():
    '''It is possible to suppress meter from dynamic measures.
    '''

    t = measuretools.DynamicMeasure("c'8 d'8 e'8 f'8")
    t.suppress_meter = True

    r'''
    {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
