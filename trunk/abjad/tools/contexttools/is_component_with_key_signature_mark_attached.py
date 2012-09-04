def is_component_with_key_signature_mark_attached(expr):
    r'''.. versionadded:: 2.3

    True when `expr` is a component with key signature mark attached::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.KeySignatureMark('c', 'major')(staff)
        KeySignatureMark(NamedChromaticPitchClass('c'), Mode('major'))(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \key c \major
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> contexttools.is_component_with_key_signature_mark_attached(staff)
        True

    Otherwise false::

        >>> contexttools.is_component_with_key_signature_mark_attached(staff[0])
        False

    Return boolean.
    '''
    from abjad.tools import contexttools

    return contexttools.is_component_with_context_mark_attached(expr, klasses=(contexttools.KeySignatureMark,))
