from abjad import *


def test_MeasuredComplexBeamSpanner_01():

    t = Staff(Measure((2, 16), notetools.make_repeated_notes(2, Duration(1, 16))) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Staff {
        {
            \time 2/16
            c'16
            d'16
        }
        {
            \time 2/16
            e'16
            f'16
        }
        {
            \time 2/16
            g'16
            a'16
        }
    }
    '''

    beam = spannertools.MeasuredComplexBeamSpanner(t[:])

    r'''
    \new Staff {
        {
            \time 2/16
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #1
            d'16
        }
        {
            \time 2/16
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #2
            e'16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #1
            f'16
        }
        {
            \time 2/16
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #2
            g'16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            a'16 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/16\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\td'16\n\t}\n\t{\n\t\t\\time 2/16\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\time 2/16\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\ta'16 ]\n\t}\n}"
