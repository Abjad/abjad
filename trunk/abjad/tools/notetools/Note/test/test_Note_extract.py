from abjad import *



def test_Note_extract_01():
    r'''Extract note.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    spannertools.GlissandoSpanner(voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 \glissando
            e'8 \glissando
            f'8 ]
        }
        '''
        )

    note = voice[1]
    note.extract()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            e'8 \glissando
            f'8 ]
        }
        '''
        )

    assert inspect(note).is_well_formed()
    assert inspect(voice).is_well_formed()


def test_Note_extract_02():
    r'''Extract multiple notes.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    spannertools.GlissandoSpanner(voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 \glissando
            e'8 \glissando
            f'8 ]
        }
        '''
        )

    notes = voice[:2]
    for note in notes:
        note.extract()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            e'8 [ \glissando
            f'8 ]
        }
        '''
        )

    for note in notes:
        assert inspect(note).is_well_formed()

    assert inspect(voice).is_well_formed()
