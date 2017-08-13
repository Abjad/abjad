import abjad


def test_spannertools_Beam__fuse_by_reference_01():
    r'''Fuse beams.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    left_beam = abjad.Beam()
    abjad.attach(left_beam, staff[:2])
    right_beam = abjad.Beam()
    abjad.attach(right_beam, staff[2:4])
    left_beam._fuse_by_reference(right_beam)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
