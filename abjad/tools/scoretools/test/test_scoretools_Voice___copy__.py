# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_scoretools_Voice___copy___01():
    r'''Voices copy name, engraver removals, engraver consists,
    grob overrides and context settings. Voices do not copy musical
    content.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_1.name = 'SopranoVoice'
    voice_1.remove_commands.append('Forbid_line_break_engraver')
    voice_1.consists_commands.append('Time_signature_engraver')
    override(voice_1).note_head.color = 'red'
    set_(voice_1).tuplet_full_length = True
    voice_2 = copy.copy(voice_1)

    assert format(voice_2) == stringtools.normalize(
        r'''
        \context Voice = "SopranoVoice" \with {
            \remove Forbid_line_break_engraver
            \consists Time_signature_engraver
            \override NoteHead.color = #red
            tupletFullLength = ##t
        } {
        }
        '''
        )


def test_scoretools_Voice___copy___02():
    r'''Voice copies semanticity flag.
    '''

    voice_1 = Voice("s8 s8 s8 s8")
    voice_1.name = 'SkipVoice'
    voice_1.is_nonsemantic = True

    assert format(voice_1) == stringtools.normalize(
        r'''
        \context Voice = "SkipVoice" {
            s8
            s8
            s8
            s8
        }
        '''
        )

    voice_2 = copy.copy(voice_1)

    assert format(voice_2) == stringtools.normalize(
        r'''
        \context Voice = "SkipVoice" {
        }
        '''
        )

    assert voice_2.is_nonsemantic
