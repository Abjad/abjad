import abjad


def test_scoretools_Container_grob_override_01():
    r'''Noncontext containers bracket grob abjad.overrides at opening and closing.
    '''

    container = abjad.Container("c'8 d'8 e'8 f'8")
    abjad.override(container).glissando.thickness = 3

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \override Glissando.thickness = #3
            c'8
            d'8
            e'8
            f'8
            \revert Glissando.thickness
        }
        '''
        )
