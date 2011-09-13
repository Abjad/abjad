from abjad import *


def test_HiddenStaffSpanner___init___01():
    '''Init empty hidden staff spanner.
    '''

    spanner = spannertools.HiddenStaffSpanner()
    assert isinstance(spanner, spannertools.HiddenStaffSpanner)


def test_HiddenStaffSpanner___init___02():
    '''Hide staff around one measure.'''

    t = Staff(Measure((2, 8), "c'8 d'8") * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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
        }
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    spannertools.HiddenStaffSpanner(t[1])

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            \stopStaff
            e'8
            f'8
            \startStaff
        }
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\t\\stopStaff\n\t\te'8\n\t\tf'8\n\t\t\\startStaff\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n}"


def test_HiddenStaffSpanner___init___03():
    '''Hide staff around one leaf.'''

    t = Note(0, (1, 8))
    spannertools.HiddenStaffSpanner(t)

    r'''
    \stopStaff
    c'8
    \startStaff
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\stopStaff\nc'8\n\\startStaff"
