from abjad.tools.voicetools.Voice import Voice
from abjad.tools import componenttools


def iterate_voices_forward_in_expr(expr):
    r'''.. versionadded:: 2.0

    Iterate voices forward in `expr`::

        abjad> voice_1 = Voice("c'8 d'8 e'8 f'8")
        abjad> voice_2 = Voice("c'4 b4")
        abjad> staff = Staff([voice_1, voice_2])
        abjad> staff.is_parallel = True

    ::

        abjad> f(staff)
        \new Staff <<
            \new Voice {
                c'8
                d'8
                e'8
                f'8
            }
            \new Voice {
                c'4
                b4
            }
        >>

    ::

        abjad> for voice in voicetools.iterate_voices_forward_in_expr(staff):
        ...   voice
        Voice{4}
        Voice{2}

    Return generator.
    '''

    return componenttools.iterate_components_forward_in_expr(expr, Voice)
