import abjad


def test_spannertools_PhrasingSlur___init___01():
    r'''Initialize empty phrasing slur.
    '''

    phrasing_slur = abjad.PhrasingSlur()
    assert isinstance(phrasing_slur, abjad.PhrasingSlur)


def test_spannertools_PhrasingSlur___init___02():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    phrasing_slur = abjad.PhrasingSlur()
    abjad.attach(phrasing_slur, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \(
            d'8
            e'8
            f'8 \)
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
