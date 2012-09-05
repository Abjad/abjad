from abjad.tools import componenttools


def iterate_voices_forward_in_expr(expr):
    r'''.. versionadded:: 2.0

    Iterate voices forward in `expr`::

        >>> voice_1 = Voice("c'8 d'8 e'8 f'8")
        >>> voice_2 = Voice("c'4 b4")
        >>> staff = Staff([voice_1, voice_2])
        >>> staff.is_parallel = True

    ::

        >>> f(staff)
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

        >>> for voice in voicetools.iterate_voices_forward_in_expr(staff):
        ...   voice
        Voice{4}
        Voice{2}

    Return generator.
    '''
    from abjad.tools import voicetools

    return componenttools.iterate_components_forward_in_expr(expr, voicetools.Voice)
