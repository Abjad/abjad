from abjad.tools.contexttools.get_dynamic_marks_attached_to_component import get_dynamic_marks_attached_to_component


def detach_dynamic_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Detach dynamic marks attached to `component`::

        abjad> staff = Staff("c'4 d'4 e'4 f'4")
        abjad> dynamic_mark = contexttools.DynamicMark('p')
        abjad> dynamic_mark.attach(staff[0])
        DynamicMark('p')(c'4)

    ::

        abjad> f(staff)
        \new Staff {
            c'4 \p
            d'4
            e'4
            f'4
        }

    ::

        abjad> contexttools.detach_dynamic_marks_attached_to_component(staff[0])
        (DynamicMark('p'),)

    ::

        abjad> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return tuple of zero or more dynamic marks.
    '''

    marks = []
    for mark in get_dynamic_marks_attached_to_component(component):
        mark.detach()
        marks.append(mark)
    return tuple(marks)
