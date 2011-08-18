from abjad import *
from abjad.tools import layouttools
from abjad.tools.leaftools._Leaf import _Leaf


def test_layouttools_set_line_breaks_cyclically_by_line_duration_ge_01():
    '''Iterate klasses in expr and accumulate prolated duration.
        Add line break after every total le line duration.'''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    layouttools.set_line_breaks_cyclically_by_line_duration_ge(t, Duration(4, 8))

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
            \break
        }
        {
            \time 2/8
            g'8
            a'8
        }
        {
            \time 2/8
            b'8
            c''8
            \break
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\break\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8\n\t\t\\break\n\t}\n}"


def test_layouttools_set_line_breaks_cyclically_by_line_duration_ge_02():
    '''Iterate klasses in expr and accumulate prolated duration.
        Add line break after every total le line duration.'''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    layouttools.set_line_breaks_cyclically_by_line_duration_ge(t, Duration(1, 8), klass = _Leaf)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            \break
            d'8
            \break
        }
        {
            \time 2/8
            e'8
            \break
            f'8
            \break
        }
        {
            \time 2/8
            g'8
            \break
            a'8
            \break
        }
        {
            \time 2/8
            b'8
            \break
            c''8
            \break
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\t\\break\n\t\td'8\n\t\t\\break\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\t\\break\n\t\tf'8\n\t\t\\break\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\t\\break\n\t\ta'8\n\t\t\\break\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb'8\n\t\t\\break\n\t\tc''8\n\t\t\\break\n\t}\n}"
