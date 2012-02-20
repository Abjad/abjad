from abjad import *


def test_DuratedComplexBeamSpanner_direction_01():
    t = Voice("c'16 d'16 e'16 f'16")
    spannertools.DuratedComplexBeamSpanner(t, durations = [(1, 8), (1, 8)], span = 1, direction='up')

    r'''
    \new Voice {
        \set stemLeftBeamCount = #0
        \set stemRightBeamCount = #2
        c'16 ^ [
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
    assert t.format == "\\new Voice {\n\t\\set stemLeftBeamCount = #0\n\t\\set stemRightBeamCount = #2\n\tc'16 ^ [\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #1\n\td'16\n\t\\set stemLeftBeamCount = #1\n\t\\set stemRightBeamCount = #2\n\te'16\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #0\n\tf'16 ]\n}"

