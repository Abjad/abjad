from abjad import *


def test_voicetools_iterate_semantic_voices_forward_in_expr_01():

    measures = measuretools.make_measures_with_full_measure_spacer_skips([(3, 8), (5, 16), (5, 16)])
    time_signature_voice = Voice(measures)
    time_signature_voice.name = 'TimeSignatureVoice'
    time_signature_voice.is_nonsemantic = True
    music_voice = Voice("c'4. d'4 e'16 f'4 g'16")
    music_voice.name = 'MusicVoice'
    staff = Staff([time_signature_voice, music_voice])
    staff.is_parallel = True

    r'''
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
    '''

    voices = voicetools.iterate_semantic_voices_forward_in_expr(staff)
    voices = list(voices)

    assert len(voices) == 1
    assert voices[0] is staff[1]
