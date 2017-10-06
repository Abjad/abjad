import abjad


def test_spannertools_Beam_direction_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
    beam = abjad.Beam(direction=abjad.Up)
    abjad.attach(beam, staff[:4])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 ^ [
            d'8
            e'8
            f'8 ]
            g'2
        }
        '''
        )


def test_spannertools_Beam_direction_02():

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
    beam = abjad.Beam(direction=abjad.Down)
    abjad.attach(beam, staff[:4])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 _ [
            d'8
            e'8
            f'8 ]
            g'2
        }
        '''
        )


def test_spannertools_Beam_direction_03():

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
    beam = abjad.Beam(direction=abjad.Center)
    abjad.attach(beam, staff[:4])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 - [
            d'8
            e'8
            f'8 ]
            g'2
        }
        '''
        )
