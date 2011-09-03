from abjad.tools.contexttools.TempoMark import TempoMark
from abjad.tools.contexttools.is_component_with_context_mark_attached import is_component_with_context_mark_attached


def is_component_with_tempo_mark_attached(expr):
    r'''.. versionadded:: 2.3

    True when `expr` is a component with tempo mark attached::

        abjad> score = Score([])
        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> score.append(staff)

    ::

        abjad> contexttools.TempoMark(Duration(1, 8), 52)(staff)
        TempoMark(8, 52)(Staff{4})

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

        abjad> contexttools.is_component_with_tempo_mark_attached(staff)
        True

    Otherwise false::

        abjad> contexttools.is_component_with_tempo_mark_attached(staff[0])
        False

    Return boolean.
    '''

    return is_component_with_context_mark_attached(expr, klasses=(TempoMark,))
