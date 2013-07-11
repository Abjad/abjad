from abjad import *


def test_Selection_detach_spanners_01():
    '''Detach tie spanners.
    '''

    staff = Staff(notetools.make_notes(0, [(5, 16), (5, 16)]))

    r'''
    \new Staff {
        c'4 ~
        c'16
        c'4 ~
        c'16
    }
    '''

    spanner_classes = (spannertools.TieSpanner,)
    staff[:].detach_spanners(spanner_classes=spanner_classes)

    r'''
    \new Staff {
        c'4
        c'16
        c'4
        c'16
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'4\n\tc'16\n\tc'4\n\tc'16\n}"


def test_Selection_detach_spanners_02():
    '''Handles empty selection without exception.
    '''

    selection = selectiontools.Selection()
    selection.detach_spanners()
