import abjad


def test_spannertools_Spanner_stop_offset_01():
    r'''Returns stop time of spanner in score.
    '''

    container = abjad.Container("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, container[1:3])
    glissando = abjad.Glissando()
    abjad.attach(glissando, container[:])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8 \glissando
            d'8 [ \glissando
            e'8 ] \glissando
            f'8
        }
        '''
        )

    assert abjad.inspect(beam).get_timespan().stop_offset == abjad.Duration(3, 8)
    assert abjad.inspect(glissando).get_timespan().stop_offset == abjad.Duration(4, 8)
