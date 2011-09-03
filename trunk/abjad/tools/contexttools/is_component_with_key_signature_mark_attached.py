from abjad.tools.contexttools.KeySignatureMark import KeySignatureMark
from abjad.tools.contexttools.is_component_with_context_mark_attached import is_component_with_context_mark_attached


def is_component_with_key_signature_mark_attached(expr):
    r'''.. versionadded:: 2.3

    True when `expr` is a component with key signature mark attached::

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

        abjad> contexttools.is_component_with_key_signature_mark_attached(staff)
        True

    Otherwise false::

        abjad> contexttools.is_component_with_key_signature_mark_attached(staff[0])
        False

    Return boolean.
    '''

    return is_component_with_context_mark_attached(expr, klasses=(KeySignatureMark,))
