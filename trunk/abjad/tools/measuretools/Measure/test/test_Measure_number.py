from abjad import *
from abjad.tools import sequencetools


def test_Measure_number_01():
    '''Measures in staff number correctly starting from 1.
    '''

    meter_pairs = [(3, 16), (5, 16), (5, 16)]
    t = Staff(measuretools.make_measures_with_full_measure_spacer_skips(meter_pairs))

    assert t[0].measure_number == 1
    assert t[1].measure_number == 2
    assert t[2].measure_number == 3


def test_Measure_number_02():
    '''Orphan measures number correctly starting from 1.
    '''

    t = Measure((3, 8), "c'8 d'8 e'8")
    assert t.measure_number == 1


def test_Measure_number_03():
    '''Mesaure numbering works correctly after contents rotation.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    assert t[0].measure_number == 1
    assert t[1].measure_number == 2
    assert t[2].measure_number == 3

    new = sequencetools.rotate_sequence(t, -1)

    r'''
    \new Staff {
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
        {
            \time 2/8
            c'8
            d'8
        }
    }
    '''

    assert new[0].measure_number == 1
    assert new[1].measure_number == 2
    assert new[2].measure_number == 3

    assert componenttools.is_well_formed_component(new)
    assert new.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n}"
