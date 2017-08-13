import abjad


def test_spannertools_TrillSpanner_pitch_01():
    r'''Works with pitch.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    trill = abjad.TrillSpanner(pitch=abjad.NamedPitch(1))
    abjad.attach(trill, staff[:2])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \pitchedTrill
            c'8 \startTrillSpan cs'
            d'8 \stopTrillSpan
            e'8
            f'8
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_TrillSpanner_pitch_02():
    r'''Works with no pitch.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    trill = abjad.TrillSpanner()
    abjad.attach(trill, staff[:2])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \startTrillSpan
            d'8 \stopTrillSpan
            e'8
            f'8
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
