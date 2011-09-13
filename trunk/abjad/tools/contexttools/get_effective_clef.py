from abjad.tools.contexttools.ClefMark import ClefMark
from abjad.tools.contexttools.get_effective_context_mark import get_effective_context_mark


def get_effective_clef(component):
    r'''.. versionadded:: 2.0

    Get effective clef of `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('treble')(staff)
        ClefMark('treble')(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \clef "treble"
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> for note in staff:
        ...     print note, contexttools.get_effective_clef(note)
        ...
        c'8 ClefMark('treble')(Staff{4})
        d'8 ClefMark('treble')(Staff{4})
        e'8 ClefMark('treble')(Staff{4})
        f'8 ClefMark('treble')(Staff{4})

    Return clef mark or none.
    '''

    return get_effective_context_mark(component, ClefMark)
