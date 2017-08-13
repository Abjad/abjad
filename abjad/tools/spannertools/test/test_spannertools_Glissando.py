import abjad


def test_spannertools_Glissando_01():

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(8)])
    glissando = abjad.Glissando()
    abjad.attach(glissando, staff[:4])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \glissando
            cs'8 \glissando
            d'8 \glissando
            ef'8
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )
