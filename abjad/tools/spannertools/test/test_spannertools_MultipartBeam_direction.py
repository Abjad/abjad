import abjad


def test_spannertools_MultipartBeam_direction_01():

    container = abjad.Container("c'8 d'8 r8 e'8 f'8 g'4")
    beam = abjad.MultipartBeam(direction=abjad.Up)
    abjad.attach(beam, container[:])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8 ^ [
            d'8 ]
            r8
            e'8 ^ [
            f'8 ]
            g'4
        }
        '''
        )

    abjad.detach(beam, container[:])
    beam = abjad.MultipartBeam(direction=abjad.Down)
    abjad.attach(beam, container[:])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8 _ [
            d'8 ]
            r8
            e'8 _ [
            f'8 ]
            g'4
        }
        '''
        )
