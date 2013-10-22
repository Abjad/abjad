# -*- encoding: utf-8 -*-


def iterate_semantic_voices_in_expr(expr, reverse=False, start=0, stop=None):
    r'''Iterate semantic voices forward in `expr`:

    ::

        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(
        ...     [(3, 8), (5, 16), (5, 16)])
        >>> time_signature_voice = Voice(measures)
        >>> time_signature_voice.name = 'TimeSignatuerVoice'
        >>> time_signature_voice.is_nonsemantic = True
        >>> music_voice = Voice("c'4. d'4 e'16 f'4 g'16")
        >>> music_voice.name = 'MusicVoice'
        >>> staff = Staff([time_signature_voice, music_voice])
        >>> staff.is_simultaneous = True

    ..  doctest::

        >>> f(staff)
        \new Staff <<
            \context Voice = "TimeSignatuerVoice" {
                {
                    \time 3/8
                    s1 * 3/8
                }
                {
                    \time 5/16
                    s1 * 5/16
                }
                {
                    s1 * 5/16
                }
            }
            \context Voice = "MusicVoice" {
                c'4.
                d'4
                e'16
                f'4
                g'16
            }
        >>

        >>> for voice in iterationtools.iterate_semantic_voices_in_expr(staff):
        ...   voice
        Voice-"MusicVoice"{5}

    Iterate semantic voices backward in `expr`:

    ::

        >>> for voice in iterationtools.iterate_semantic_voices_in_expr(staff, reverse=True):
        ...   voice
        Voice-"MusicVoice"{5}

    Returns generator.
    '''
    from abjad.tools import iterationtools

    for voice in iterationtools.iterate_voices_in_expr(
        expr, reverse=reverse, start=start, stop=stop):
        if not voice.is_nonsemantic:
            yield voice
