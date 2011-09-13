from abjad import *


def test_Spanner_fracture_01():
    '''Fracture container spanner to the right of index 1.'''

    t = Staff(Container(notetools.make_repeated_notes(4)) * 3)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner(t[:])
    original, left, right = p.fracture(1, 'right')

    assert len(original.components) == 3
    assert original.components[0] is t[0]
    assert original.components[1] is t[1]
    assert original.components[2] is t[2]
    assert len(original.leaves) == 12

    assert len(left.components) == 2
    assert left.components[0] is t[0]
    assert left.components[1] is t[1]
    assert len(left.leaves) == 8

    assert len(right.components) == 1
    assert right.components[0] is t[2]
    assert len(right.leaves) == 4

    assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tcs'8\n\t\td'8\n\t\tef'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\tg'8 ]\n\t}\n\t{\n\t\taf'8 [\n\t\ta'8\n\t\tbf'8\n\t\tb'8 ]\n\t}\n}"

    r'''
    \new Staff {
        {
            c'8 [
            cs'8
            d'8
            ef'8
        }
        {
            e'8
            f'8
            fs'8
            g'8 ]
        }
        {
            af'8 [
            a'8
            bf'8
            b'8 ]
        }
    }
    '''
