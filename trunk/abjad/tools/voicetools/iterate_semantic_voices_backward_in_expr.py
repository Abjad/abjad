def iterate_semantic_voices_backward_in_expr(expr):
    r'''.. versionadded:: 2.0

    Iterate semantic voices backward in `expr`::

        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(
        ...     [(3, 8), (5, 16), (5, 16)])
        >>> time_signature_voice = Voice(measures)
        >>> time_signature_voice.name = 'TimeSignatureVoice'
        >>> time_signature_voice.is_nonsemantic = True
        >>> music_voice = Voice("c'4. d'4 e'16 f'4 g'16")
        >>> music_voice.name = 'MusicVoice'
        >>> staff = Staff([time_signature_voice, music_voice])
        >>> staff.is_parallel = True

    ::

        >>> f(staff)
        \new Staff <<
            \context Voice = "TimeSignatureVoice" {
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

        >>> for voice in voicetools.iterate_semantic_voices_backward_in_expr(staff):
        ...   voice
        Voice-"MusicVoice"{5}

    Return generator.
    '''
    from abjad.tools import voicetools

    for voice in voicetools.iterate_voices_backward_in_expr(expr):
        if not voice.is_nonsemantic:
            yield voice
