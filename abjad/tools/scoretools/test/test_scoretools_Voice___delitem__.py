from abjad import *


def test_scoretools_Voice___delitem___01():
    r'''Delete container from voice.
    '''

    voice = Voice(r'''
        c'8 [ \glissando
        {
            d'8 \glissando
            e'8 \glissando
        }
        f'8 ]
        ''')

    assert format(voice) == stringtools.normalize(
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

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [ \glissando
            f'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()
    assert inspect_(container).is_well_formed()
