from abjad import *


def test_DynamicMeasure_denominator_01():
    '''You can control the denominator of dynamic measures.
    '''

    t = measuretools.DynamicMeasure("c'8 d'8 e'8 f'8")
    t.denominator = 32

    assert contexttools.get_effective_time_signature(t) == (16, 32)

    r'''
    {
        \time 16/32
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "{\n\t\\time 16/32\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_DynamicMeasure_denominator_02():
    '''Bad denominator values have no effect.
    '''

    t = measuretools.DynamicMeasure("c'8 d'8 e'8 f'8")
    t.denominator = 117

    r'''
    {
        \time 1/2
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "{\n\t\\time 1/2\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
