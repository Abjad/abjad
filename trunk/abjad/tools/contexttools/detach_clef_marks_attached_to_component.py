from abjad.tools.contexttools.get_clef_marks_attached_to_component import get_clef_marks_attached_to_component


def detach_clef_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Detach clef marks attached to `component`::

        abjad> staff = Staff("c'4 d'4 e'4 f'4")
        abjad> clef_mark = contexttools.ClefMark('treble')
        abjad> clef_mark.attach(staff)
        ClefMark('treble')(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \clef "treble"
            c'4
            d'4
            e'4
            f'4
        }

    ::

        abjad> contexttools.detach_clef_marks_attached_to_component(staff)
        (ClefMark('treble'),)

    ::

        abjad> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return tuple of zero or more clef marks.
    '''

    marks = []
    for mark in get_clef_marks_attached_to_component(component):
        mark.detach()
        marks.append(mark)
    return tuple(marks)
