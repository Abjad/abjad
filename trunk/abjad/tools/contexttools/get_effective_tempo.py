from abjad.tools.contexttools.TempoMark import TempoMark
from abjad.tools.contexttools.get_effective_context_mark import get_effective_context_mark


def get_effective_tempo(component):
    r'''.. versionadded:: 2.0

    Get effective tempo of `component`::

        abjad> score = Score([])
        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> score.append(staff)
        abjad> contexttools.TempoMark(Duration(1, 8), 52)(staff[0])
        TempoMark(8, 52)(c'8)

    ::

        abjad> f(score)
        \new Score <<
            \tempo 8=52
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
        >>

    ::

        abjad> for note in staff:
        ...     print note, contexttools.get_effective_tempo(note)
        ...
        c'8 TempoMark(8, 52)(c'8)
        d'8 TempoMark(8, 52)(c'8)
        e'8 TempoMark(8, 52)(c'8)
        f'8 TempoMark(8, 52)(c'8)

    Return tempo mark or none.
    '''

    return get_effective_context_mark(component, TempoMark)
