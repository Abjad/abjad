import abjad


def test_spannertools_ComplexBeam_direction_01():

    staff = abjad.Staff("c'16 e'16 r16 f'16 g'2")
    beam = abjad.ComplexBeam(direction=abjad.Up)
    abjad.attach(beam, staff[:4])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 ^ [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #2
            e'16 ]
            r16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            f'16 ^ [ ]
            g'2
        }
        '''
        )


def test_spannertools_ComplexBeam_direction_02():

    staff = abjad.Staff("c'16 e'16 r16 f'16 g'2")
    beam = abjad.ComplexBeam(direction=abjad.Down)
    abjad.attach(beam, staff[:4])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 _ [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #2
            e'16 ]
            r16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            f'16 _ [ ]
            g'2
        }
        '''
        )
