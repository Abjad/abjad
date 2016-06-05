# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_IterationAgent_by_semantic_voice_01():

    durations = [(3, 8), (5, 16), (5, 16)]
    measures = scoretools.make_spacer_skip_measures(durations)
    time_signature_voice = Voice(measures)
    time_signature_voice.name = 'TimeSignatureVoice'
    time_signature_voice.is_nonsemantic = True
    music_voice = Voice("c'4. d'4 e'16 f'4 g'16")
    music_voice.name = 'MusicVoice'
    staff = Staff([time_signature_voice, music_voice])
    staff.is_simultaneous = True

    assert format(staff) == stringtools.normalize(
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
        )

    voices = iterate(staff).by_semantic_voice(reverse=True)
    voices = list(voices)

    assert len(voices) == 1
    assert voices[0] is staff[1]


def test_agenttools_IterationAgent_by_semantic_voice_02():

    durations = [(3, 8), (5, 16), (5, 16)]
    measures = scoretools.make_spacer_skip_measures(durations)
    time_signature_voice = Voice(measures)
    time_signature_voice.name = 'TimeSignatureVoice'
    time_signature_voice.is_nonsemantic = True
    music_voice = Voice("c'4. d'4 e'16 f'4 g'16")
    music_voice.name = 'MusicVoice'
    staff = Staff([time_signature_voice, music_voice])
    staff.is_simultaneous = True

    assert format(staff) == stringtools.normalize(
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
        )

    voices = iterate(staff).by_semantic_voice()
    voices = list(voices)

    assert len(voices) == 1
    assert voices[0] is staff[1]
