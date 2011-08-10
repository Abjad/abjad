from abjad.tools.voicetools.Voice import Voice
from abjad.tools import componenttools


def iterate_semantic_voices_forward_in_expr(expr):
    r'''.. versionadded:: 2.0

    Iterate semantic voices forward in `expr`::

        abjad> measures = measuretools.make_measures_with_full_measure_spacer_skips([(3, 8), (5, 16), (5, 16)])
        abjad> meter_voice = Voice(measures)
        abjad> meter_voice.name = 'TimeSignatuerVoice'
        abjad> meter_voice.is_nonsemantic = True
        abjad> music_voice = Voice("c'4. d'4 e'16 f'4 g'16")
        abjad> music_voice.name = 'MusicVoice'
        abjad> staff = Staff([meter_voice, music_voice])
        abjad> staff.is_parallel = True

    ::

        abjad> f(staff)
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
                    \time 5/16
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

        abjad> for voice in voicetools.iterate_semantic_voices_forward_in_expr(staff):
        ...   voice
        Voice-"MusicVoice"{5}

    Return generator.
    '''

    for voice in componenttools.iterate_components_forward_in_expr(expr, Voice):
        if not voice.is_nonsemantic:
            yield voice
