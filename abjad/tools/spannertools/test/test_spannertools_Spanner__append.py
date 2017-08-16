import abjad


def test_spannertools_Spanner__append_01():
    r'''Append one container to the right.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = abjad.Beam()
    abjad.attach(beam, voice[1][:])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8 [
                f'8 ]
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    beam._append(voice[2][0])
    beam._append(voice[2][1])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8 [
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )


def test_spannertools_Spanner__append_02():
    r'''Append one leaf to the right.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = abjad.Beam()
    abjad.attach(beam, voice[1][:])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8 [
                f'8 ]
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    beam._append(voice[2][0])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8 [
                f'8
            }
            {
                g'8 ]
                a'8
            }
        }
        '''
        )
