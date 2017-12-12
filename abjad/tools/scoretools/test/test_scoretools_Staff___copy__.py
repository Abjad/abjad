import abjad
import copy


def test_scoretools_Staff___copy___01():
    r'''Staves (shallow) copy grob abjad.overrides and context abjad.settings
    but not components.
    '''

    staff_1 = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff_1).note_head.color = 'red'
    abjad.setting(staff_1).tuplet_full_length = True


    staff_2 = copy.copy(staff_1)

    assert format(staff_2) == abjad.String.normalize(
        r'''
        \new Staff \with {
            \override NoteHead.color = #red
            tupletFullLength = ##t
        } {
        }
        '''
        )
