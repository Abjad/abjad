from abjad.tools.marktools.get_noncontext_marks_attached_to_component import get_noncontext_marks_attached_to_component


def detach_noncontext_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Detach noncontext marks attached to `component`::


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

        abjad> marktools.detach_noncontext_marks_attached_to_component(staff[0])
        (Articulation('staccato'),)

    ::

        abjad> f(staff)
        \new Staff {
            \time 2/4
            c'8
            d'8
            e'8
            f'8
        }

    Return tuple of noncontext marks.
    '''

    noncontext_marks = []
    for noncontext_mark in get_noncontext_marks_attached_to_component(component):
        noncontext_mark.detach()
        noncontext_marks.append(noncontext_mark)

    return tuple(noncontext_marks)
