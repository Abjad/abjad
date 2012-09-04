def get_key_signature_mark_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get key signature mark attached to `component`::

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

        >>> contexttools.get_key_signature_mark_attached_to_component(staff)
        KeySignatureMark(NamedChromaticPitchClass('c'), Mode('major'))(Staff{4})

    Return key signature mark.

    Raise missing mark error when no key signature mark attaches to component.
    '''
    from abjad.tools import contexttools

    return contexttools.get_context_mark_attached_to_component(component, klasses=(contexttools.KeySignatureMark,))
