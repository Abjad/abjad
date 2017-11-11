import abjad


def test_spannertools_MeasuredComplexBeam_direction_01():

    staff = abjad.Staff(
        "abj: | 2/16 c'16 d'16 || 2/16 e'16 f'16 |"
        "| 2/16 g'16 a'16 |"
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/16
                c'16
                d'16
            } % measure
            { % measure
                e'16
                f'16
            } % measure
            { % measure
                g'16
                a'16
            } % measure
        }
        '''
        )

    leaves = abjad.select(staff).leaves()
    beam = abjad.MeasuredComplexBeam(direction=abjad.Down)
    abjad.attach(beam, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/16
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #2
                c'16 _ [
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #1
                d'16
            } % measure
            { % measure
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #2
                e'16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #1
                f'16
            } % measure
            { % measure
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #2
                g'16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #0
                a'16 ]
            } % measure
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
