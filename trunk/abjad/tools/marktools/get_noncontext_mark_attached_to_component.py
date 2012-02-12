from abjad.tools.marktools.get_noncontext_marks_attached_to_component import get_noncontext_marks_attached_to_component


def get_noncontext_mark_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get exactly one noncontext_mark attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> marktools.Articulation('staccato')(staff[0])
        Articulation('staccato')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 -\staccato
            d'8
            e'8
            f'8
        }

    ::

        abjad> marktools.get_noncontext_mark_attached_to_component(staff[0])
        Articulation('staccato')(c'8)

    Return one noncontext_mark.

    Raise missing mark error when no noncontext_mark is attached.

    Raise extra mark error when more than one noncontext_mark is attached.
    '''

    noncontext_marks = get_noncontext_marks_attached_to_component(component)
    if not noncontext_marks:
        raise MissingMarkError
    elif 1 < len(noncontext_marks):
        raise ExtraMarkError
    else:
        return noncontext_marks[0]
