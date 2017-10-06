import abjad


def test_spannertools_PhrasingSlur_direction_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    slur = abjad.PhrasingSlur(direction=abjad.Up)
    abjad.attach(slur, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 ^ \(
            d'8
            e'8
            f'8 \)
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_PhrasingSlur_direction_02():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    slur = abjad.PhrasingSlur(direction=abjad.Down)
    abjad.attach(slur, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 _ \(
            d'8
            e'8
            f'8 \)
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
