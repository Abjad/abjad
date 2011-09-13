from abjad import *


def test_Spanner_extend_01():
    '''Extend spanner to the right.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner(t[1])

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        {
            e'8 [
            f'8 ]
        }
        {
            g'8
            a'8
        }
    }
    '''

    p.extend(t[2][:])

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        {
            e'8 [
            f'8
        }
        {
            g'8
            a'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8 [\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"


def test_Spanner_extend_02():
    '''Extend spanner to the right.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner(t[1])

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        {
            e'8 [
            f'8 ]
        }
        {
            g'8
            a'8
        }
    }
    '''

    p.extend(t[2:])

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        {
            e'8 [
            f'8
        }
        {
            g'8
            a'8 ]
        }
    }
    '''

    assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8 [\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
