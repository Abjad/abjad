import abjad


def test_spannertools_ComplexBeam___init___01():
    r'''Initialize empty complex beam spanner.
    '''

    beam = abjad.ComplexBeam()
    assert isinstance(beam, abjad.ComplexBeam)


def test_spannertools_ComplexBeam___init___02():

    staff = abjad.Staff("c'16 e'16 r16 f'16 g'2")
    beam = abjad.ComplexBeam()
    abjad.attach(beam, staff[:4])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #2
            e'16 ]
            r16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            f'16 [ ]
            g'2
        }
        '''
        )
