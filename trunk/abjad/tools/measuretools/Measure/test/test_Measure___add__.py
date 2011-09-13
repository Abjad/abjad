from abjad import *


def test_Measure___add___01():
    '''Add outside-of-score rigid measures.'''

    t1 = Measure((1, 8), "c'16 d'16")
    spannertools.BeamSpanner(t1[:])
    t2 = Measure((2, 16), "c'16 d'16")
    spannertools.SlurSpanner(t2[:])

    r'''
    {
        \time 1/8
        c'16 [
        d'16 ]
    }
    '''

    r'''
    {
        \time 2/16
        c'16 (
        d'16 )
    }
    '''

    new = t1 + t2

    r'''
    {
        \time 2/8
        c'16 [
        d'16 ]
        c'16 (
        d'16 )
    }
    '''

    assert new is not t1 and new is not t2
    assert len(t1) == 0
    assert len(t2) == 0
    assert componenttools.is_well_formed_component(new)
    assert new.format == "{\n\t\\time 2/8\n\tc'16 [\n\td'16 ]\n\tc'16 (\n\td'16 )\n}"


def test_Measure___add___02():
    '''Add rigid measures in score.'''

    t1 = Measure((1, 8), "c'16 d'16")
    spannertools.BeamSpanner(t1[:])
    t2 = Measure((2, 16), "c'16 d'16")
    spannertools.SlurSpanner(t2[:])
    t = Staff([t1, t2])

    r'''
    \new Staff {
        {
            \time 1/8
            c'16 [
            d'16 ]
        }
        {
            \time 2/16
            c'16 (
            d'16 )
        }
    }
    '''

    new = t1 + t2

    r'''
    {
        \time 2/8
        c'16 [
        d'16 ]
        c'16 (
        d'16 )
    }
    '''

    assert new is not t1 and new is not t2
    assert len(t1) == 0
    assert len(t2) == 0
    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16 [\n\t\td'16 ]\n\t\tc'16 (\n\t\td'16 )\n\t}\n}"
