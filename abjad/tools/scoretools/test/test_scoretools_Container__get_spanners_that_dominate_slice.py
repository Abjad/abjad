import abjad


def test_scoretools_Container__get_spanners_that_dominate_slice_01():
    r'''Get dominant spanners over zero-length slice.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:2])
    glissando = abjad.Glissando()
    abjad.attach(glissando, voice[:])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 ] \glissando
            e'8 \glissando
            f'8
        }
        '''
        )

    receipt = voice._get_spanners_that_dominate_slice(2, 2)

    assert len(receipt) == 1
    assert (glissando, 2) in receipt


def test_scoretools_Container__get_spanners_that_dominate_slice_02():
    r'''Get dominant spanners over one-component slice.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:2])
    glissando = abjad.Glissando()
    abjad.attach(glissando, voice[:])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 ] \glissando
            e'8 \glissando
            f'8
        }
        '''
        )

    receipt = voice._get_spanners_that_dominate_slice(1, 2)

    assert len(receipt) == 2
    assert (beam, 1) in receipt
    assert (glissando, 1) in receipt


def test_scoretools_Container__get_spanners_that_dominate_slice_03():
    r'''Get dominant spanners over four-component slice.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:2])
    glissando = abjad.Glissando()
    abjad.attach(glissando, voice[:])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 ] \glissando
            e'8 \glissando
            f'8
        }
        '''
        )

    receipt = voice._get_spanners_that_dominate_slice(0, 4)

    assert len(receipt) == 1
    assert (glissando, 0) in receipt
