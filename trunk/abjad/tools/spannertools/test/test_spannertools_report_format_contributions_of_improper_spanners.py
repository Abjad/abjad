from abjad import *


def test_spannertools_report_format_contributions_of_improper_spanners_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = beamtools.BeamSpanner(staff.leaves)
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

    r'''
    BeamSpanner
        _format_right_of_leaf
            [
    SlurSpanner
        _format_right_of_leaf
            (
    TrillSpanner
        _format_right_of_leaf
            \startTrillSpan
    '''

    assert spannertools.report_format_contributions_of_improper_spanners(staff[0]) == 'BeamSpanner\n\t_format_right_of_leaf\n\t\t[\nSlurSpanner\n\t_format_right_of_leaf\n\t\t(\nTrillSpanner\n\t_format_right_of_leaf\n\t\t\\startTrillSpan\n'
