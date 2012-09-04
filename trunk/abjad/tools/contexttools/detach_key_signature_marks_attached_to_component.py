def detach_key_signature_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Detach key signature marks attached to `component`::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> key_signature_mark = contexttools.KeySignatureMark('c', 'major')
        >>> key_signature_mark.attach(staff)
        KeySignatureMark(NamedChromaticPitchClass('c'), Mode('major'))(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \key c \major
            c'4
            d'4
            e'4
            f'4
        }

    ::

        >>> contexttools.detach_key_signature_marks_attached_to_component(staff)
        (KeySignatureMark(NamedChromaticPitchClass('c'), Mode('major')),)

    ::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return tuple of zero or more key signature marks.
    '''
    from abjad.tools import contexttools

    marks = []
    for mark in contexttools.get_key_signature_marks_attached_to_component(component):
        mark.detach()
        marks.append(mark)

    return tuple(marks)
