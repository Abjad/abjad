from abjad import *


def test__NavigationInterface_contemporaneous_start_components_01( ):
    '''Notes.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8
        }
    }
    '''

    assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"

    result = t._navigator._contemporaneous_start_components

    "[Voice{3}, Container(c'8, d'8), Note(c', 8)]"

    assert len(result) == 3
    assert t in result
    assert t[0] in result
    assert t[0][0] in result

    result = t[0]._navigator._contemporaneous_start_components

    "[Container(c'8, d'8), Note(c', 8), Voice{3}]"

    assert len(result) == 3
    assert t in result
    assert t[0] in result
    assert t[0][0] in result

    result = t[0][0]._navigator._contemporaneous_start_components

    "[Note(c', 8), Container(c'8, d'8), Voice{3}]"

    assert len(result) == 3
    assert t in result
    assert t[0] in result
    assert t[0][0] in result


# NONSTRUCTURAL in new parallel --> context model.
#def test__NavigationInterface_contemporaneous_start_components_02( ):
#   '''With parallel containers.'''
#
#   t = Voice([Container(Container(notetools.make_repeated_notes(2)) * 2)] + notetools.make_repeated_notes(2))
#   t[0].is_parallel = True
#   pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
#
#   r'''\new Voice {
#      <<
#         {
#            c'8
#            d'8
#         }
#         {
#            e'8
#            f'8
#         }
#      >>
#      g'8
#      a'8
#   }'''
#
#   assert t.format == "\\new Voice {\n\t<<\n\t\t{\n\t\t\tc'8\n\t\t\td'8\n\t\t}\n\t\t{\n\t\t\te'8\n\t\t\tf'8\n\t\t}\n\t>>\n\tg'8\n\ta'8\n}"
#
#   result = t._navigator._contemporaneous_start_components
#
#   "[Container(Container(c'8, d'8), Container(e'8, f'8)), Note(e', 8), Container(c'8, d'8), Voice{3}, Note(c', 8), Container(e'8, f'8)]"
#
#   assert len(result) == 6
#   assert t in result
#   assert t[0] in result
#   assert t[0][0] in result
#   assert t[0][0][0] in result
#   assert t[0][1] in result
#   assert t[0][1][0] in result
