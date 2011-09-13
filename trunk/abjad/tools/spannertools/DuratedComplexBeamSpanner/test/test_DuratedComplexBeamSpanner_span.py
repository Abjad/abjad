from abjad import *


def test_DuratedComplexBeamSpanner_span_01():
    '''1-beam span between adjacent groups of 1/16th notes.'''

    t = Voice("c'16 d'16 e'16 f'16")
    spannertools.DuratedComplexBeamSpanner(t, durations = [(1, 8), (1, 8)], span = 1)

    r'''
    \new Voice {
        \set stemLeftBeamCount = #0
        \set stemRightBeamCount = #2
        c'16 [
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #1
        d'16
        \set stemLeftBeamCount = #1
        \set stemRightBeamCount = #2
        e'16
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #0
        f'16 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t\\set stemLeftBeamCount = #0\n\t\\set stemRightBeamCount = #2\n\tc'16 [\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #1\n\td'16\n\t\\set stemLeftBeamCount = #1\n\t\\set stemRightBeamCount = #2\n\te'16\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #0\n\tf'16 ]\n}"



def test_DuratedComplexBeamSpanner_span_02():
    '''2-beam span between adjacent groups of 1/16th notes.'''

    t = Voice("c'16 d'16 e'16 f'16")
    spannertools.DuratedComplexBeamSpanner(t, durations = [(1, 8), (1, 8)], span = 2)

    r'''
    \new Voice {
        \set stemLeftBeamCount = #0
        \set stemRightBeamCount = #2
        c'16 [
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #2
        d'16
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #2
        e'16
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #0
        f'16 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t\\set stemLeftBeamCount = #0\n\t\\set stemRightBeamCount = #2\n\tc'16 [\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #2\n\td'16\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #2\n\te'16\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #0\n\tf'16 ]\n}"
