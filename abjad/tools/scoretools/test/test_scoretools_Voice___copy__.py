import abjad
import copy


def test_scoretools_Voice___copy___01():
    r'''Voices copy name, engraver removals, engraver consists,
    grob abjad.overrides and context abjad.settings. Voices do not copy
    components.
    '''

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_1.name = 'SopranoVoice'
    voice_1.remove_commands.append('Forbid_line_break_engraver')
    voice_1.consists_commands.append('Time_signature_engraver')
    abjad.override(voice_1).note_head.color = 'red'
    abjad.setting(voice_1).tuplet_full_length = True
    voice_2 = copy.copy(voice_1)

    assert format(voice_2) == abjad.String.normalize(
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
