def get_effective_key_signature(component):
    r'''.. versionadded:: 2.0

    Get effective key signature of `component`::

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

        >>> for note in staff:
        ...     note, contexttools.get_effective_key_signature(note)
        ...
        (Note("c'8"), KeySignatureMark(NamedChromaticPitchClass('c'), Mode('major'))(Staff{4}))
        (Note("d'8"), KeySignatureMark(NamedChromaticPitchClass('c'), Mode('major'))(Staff{4}))
        (Note("e'8"), KeySignatureMark(NamedChromaticPitchClass('c'), Mode('major'))(Staff{4}))
        (Note("f'8"), KeySignatureMark(NamedChromaticPitchClass('c'), Mode('major'))(Staff{4}))

    Return key signature mark or none.
    '''
    from abjad.tools import contexttools

    return contexttools.get_effective_context_mark(component, contexttools.KeySignatureMark)
