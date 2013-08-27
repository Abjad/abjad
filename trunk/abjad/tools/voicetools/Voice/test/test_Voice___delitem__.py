from abjad import *


def test_Voice___delitem___01():
    r'''Delete container from voice.
    '''

    voice = Voice(notetools.make_repeated_notes(2))
    voice.insert(1, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    spannertools.BeamSpanner(voice.select_leaves())
    spannertools.GlissandoSpanner(voice.select_leaves())

    testtools.compare(
        voice,
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

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            f'8 ]
        }
        '''
        )

    assert inspect(voice).is_well_formed()
    assert inspect(container).is_well_formed()
