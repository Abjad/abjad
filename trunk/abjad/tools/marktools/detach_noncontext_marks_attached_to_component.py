def detach_noncontext_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Detach noncontext marks attached to `component`::


        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.TimeSignatureMark((2, 4))(staff[0])
        TimeSignatureMark((2, 4))(c'8)
        >>> marktools.Articulation('staccato')(staff[0])
        Articulation('staccato')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            \time 2/4
            c'8 -\staccato
            d'8
            e'8
            f'8
        }

    ::

        >>> marktools.detach_noncontext_marks_attached_to_component(staff[0])
        (Articulation('staccato'),)

    ::

        >>> f(staff)
        \new Staff {
            \time 2/4
            c'8
            d'8
            e'8
            f'8
        }

    Return tuple of noncontext marks.
    '''
    from abjad.tools import marktools

    noncontext_marks = []
    for noncontext_mark in marktools.get_noncontext_marks_attached_to_component(component):
        noncontext_mark.detach()
        noncontext_marks.append(noncontext_mark)

    return tuple(noncontext_marks)
