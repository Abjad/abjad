import abjad


def test_scoretools_Voice___delitem___01():
    r'''Delete container from voice.
    '''

    voice = abjad.Voice(r'''
        c'8 [ \glissando
        {
            d'8 \glissando
            e'8 \glissando
        }
        f'8 ]
        ''')

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [ \glissando
            {
                d'8 \glissando
                e'8 \glissando
            }
            f'8 ]
        }
        '''
        )

    container = voice[1]
    del(voice[1:2])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [ \glissando
            f'8 ]
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()
    assert abjad.inspect(container).is_well_formed()
