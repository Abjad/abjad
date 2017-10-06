import abjad


def test_scoretools_LogicalTie__add_or_remove_notes_to_achieve_written_duration_01():
    r'''Change trivial logical tie to nontrivial logical tie.
    '''

    staff = abjad.Staff("c'8 [ ]")
    logical_tie = abjad.inspect(staff[0]).get_logical_tie()
    logical_tie._add_or_remove_notes_to_achieve_written_duration(abjad.Duration(5, 32))

    r'''
    \new Staff {
        c'8 ~ [
        c'32 ]
    }
    '''

    assert abjad.inspect(staff).is_well_formed()
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 ~ [
            c'32 ]
        }
        '''
        )


def test_scoretools_LogicalTie__add_or_remove_notes_to_achieve_written_duration_02():
    r'''Change nontrivial logical tie to trivial logical tie.
    '''

    staff = abjad.Staff("c'8 ~ [ c'32 ]")
    logical_tie = abjad.inspect(staff[0]).get_logical_tie()
    logical_tie._add_or_remove_notes_to_achieve_written_duration(abjad.Duration(1, 8))

    r'''
    \new Staff {
        c'8 [ ]
    }
    '''

    assert abjad.inspect(staff).is_well_formed()
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 [ ]
        }
        '''
        )
