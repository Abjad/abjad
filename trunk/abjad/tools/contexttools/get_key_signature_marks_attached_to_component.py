from abjad.tools.contexttools.KeySignatureMark import KeySignatureMark
from abjad.tools.contexttools.get_context_marks_attached_to_component import get_context_marks_attached_to_component


def get_key_signature_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get key signature marks attached to `component`::

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

        abjad> contexttools.get_key_signature_marks_attached_to_component(staff)
        (KeySignatureMark(NamedChromaticPitchClass('c'), Mode(major))(Staff{4}),)

    Return tuple of zero or more key signature marks.
    '''

    return get_context_marks_attached_to_component(component, klasses=(KeySignatureMark,))
