from abjad.tools.contexttools.get_time_signature_mark_attached_to_component import get_time_signature_mark_attached_to_component


def detach_time_signature_mark_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Detach time signature mark attached to `component`::

        abjad> staff = Staff("c'4 d'4 e'4 f'4")
        abjad> contexttools.TimeSignatureMark(4, 4)(staff[0])
        TimeSignatureMark(4, 4)(c'4)

    ::

        abjad> f(staff)
        \new Staff {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
        }

    ::

        abjad> contexttools.detach_time_signature_mark_attached_to_component(staff[0])
        TimeSignatureMark(4, 4)

    ::

        abjad> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return time signature mark.

    Raise missing mark error when no time signature mark attached to `component`.
    '''

    time_signature_mark = get_time_signature_mark_attached_to_component(component)

    return time_signature_mark.detach_mark()


