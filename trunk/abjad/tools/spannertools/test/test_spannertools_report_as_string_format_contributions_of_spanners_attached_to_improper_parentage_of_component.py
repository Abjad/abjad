from abjad import *


def test_spannertools_report_as_string_format_contributions_of_spanners_attached_to_improper_parentage_of_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff.leaves)
    slur = spannertools.SlurSpanner(staff.leaves)
    trill = spannertools.TrillSpanner(staff)

    r'''
    \new Staff {
        c'8 [ ( \startTrillSpan
        d'8
        e'8
        f'8 ] ) \stopTrillSpan
    }
    '''

    assert spannertools.report_as_string_format_contributions_of_all_spanners_attached_to_improper_parentage_of_component(staff[0]) == 'BeamSpanner\n\t_right\n\t\t[\nSlurSpanner\n\t_right\n\t\t(\nTrillSpanner\n\t_right\n\t\t\\startTrillSpan\n'
