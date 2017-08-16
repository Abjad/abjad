import abjad


def test_scoretools_Tuplet_grob_override_01():
    r'''Tuplets bracket grob abjad.overrides at before and after slots.
    '''

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8 f'8")
    abjad.override(tuplet).glissando.thickness = 3

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \override Glissando.thickness = #3
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            c'8
            d'8
            e'8
            f'8
        }
        \revert Glissando.thickness
        '''
        )
