from abjad.tools.marktools.get_marks_attached_to_component import get_marks_attached_to_component


def get_noncontext_marks_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get noncontext marks attached to component::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.TimeSignatureMark((2, 4))(staff[0])
        TimeSignatureMark((2, 4))(c'8)
        abjad> marktools.Articulation('staccato')(staff[0])
        Articulation('staccato')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            \time 2/4
            c'8 -\staccato
            d'8
            e'8
            f'8
        }

    ::

        abjad> marktools.get_noncontext_marks_attached_to_component(staff[0])
        (Articulation('staccato')(c'8),)

    Return tuple of zero or more marks.
    '''
    from abjad.tools import contexttools

    result = []

    for mark in get_marks_attached_to_component(component):
        if not isinstance(mark, contexttools.ContextMark):
            result.append(mark)

    return tuple(result)
