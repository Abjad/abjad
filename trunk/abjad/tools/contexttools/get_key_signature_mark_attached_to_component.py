from abjad.tools.contexttools.KeySignatureMark import KeySignatureMark
from abjad.tools.contexttools.get_context_mark_attached_to_component import get_context_mark_attached_to_component


def get_key_signature_mark_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get key signature mark attached to `component`::

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

        abjad> contexttools.get_key_signature_mark_attached_to_component(staff)
        KeySignatureMark(NamedChromaticPitchClass('c'), Mode(major))(Staff{4})

    Return key signature mark.

    Raise missing mark error when no key signature mark attaches to component.
    '''

    return get_context_mark_attached_to_component(component, klasses=(KeySignatureMark,))
