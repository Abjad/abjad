from abjad.tools.contexttools.KeySignatureMark import KeySignatureMark
from abjad.tools.contexttools.get_effective_context_mark import get_effective_context_mark


def get_effective_key_signature(component):
    r'''.. versionadded:: 2.0

    Get effective key signature of `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.KeySignatureMark('c', 'major')(staff)
        KeySignatureMark(NamedChromaticPitchClass('c'), Mode(major))(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \key c \major
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> for note in staff:
        ...     note, contexttools.get_effective_key_signature(note)
        ...
        (Note("c'8"), KeySignatureMark(NamedChromaticPitchClass('c'), Mode(major))(Staff{4}))
        (Note("d'8"), KeySignatureMark(NamedChromaticPitchClass('c'), Mode(major))(Staff{4}))
        (Note("e'8"), KeySignatureMark(NamedChromaticPitchClass('c'), Mode(major))(Staff{4}))
        (Note("f'8"), KeySignatureMark(NamedChromaticPitchClass('c'), Mode(major))(Staff{4}))

    Return key signature mark or none.
    '''

    return get_effective_context_mark(component, KeySignatureMark)
