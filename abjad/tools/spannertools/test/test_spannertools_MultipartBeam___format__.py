import abjad


def test_spannertools_MultipartBeam___format___01():

    container = abjad.Container("c'8 d'8 r8 e'8 f'8 g'4")
    beam = abjad.MultipartBeam()
    abjad.attach(beam, container[:])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8 [
            d'8 ]
            r8
            e'8 [
            f'8 ]
            g'4
        }
        '''
        )


def test_spannertools_MultipartBeam___format___02():

    container = abjad.Container("c'8 r4 c'8")
    beam = abjad.MultipartBeam()
    abjad.attach(beam, container[:])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8
            r4
            c'8
        }
        '''
        )


def test_spannertools_MultipartBeam___format___03():

    container = abjad.Container("c'8. r16 c'8. r16")
    beam = abjad.MultipartBeam()
    abjad.attach(beam, container[:])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8.
            r16
            c'8.
            r16
        }
        '''
        )
