import abjad
import pytest


def test_scoretools_Mutation_replace_measure_contents_01():
    r'''Contents duration less than sum of duration of measures.
    abjad.Note spacer skip at end of second measure.
    '''

    maker = abjad.MeasureMaker()
    measures = maker([(1, 8), (3, 16)])
    staff = abjad.Staff(measures)
    notes = [abjad.Note("c'16"), abjad.Note("d'16"), abjad.Note("e'16"), abjad.Note("f'16")]
    abjad.mutate(staff).replace_measure_contents(notes)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 1/8
                c'16
                d'16
            } % measure
            { % measure
                \time 3/16
                e'16
                f'16
                s1 * 1/16
            } % measure
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Mutation_replace_measure_contents_02():
    r'''Some contents too big for some measures.
    Small measures skipped.
    '''

    time_signatures = [(1, 16), (3, 16), (1, 16), (3, 16)]
    maker = abjad.MeasureMaker()
    measures = maker(time_signatures)
    staff = abjad.Staff(measures)
    notes = [abjad.Note("c'8"), abjad.Note("d'8")]
    abjad.mutate(staff).replace_measure_contents(notes)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 1/16
                s1 * 1/16
            } % measure
            { % measure
                \time 3/16
                c'8
                s1 * 1/16
            } % measure
            { % measure
                \time 1/16
                s1 * 1/16
            } % measure
            { % measure
                \time 3/16
                d'8
                s1 * 1/16
            } % measure
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Mutation_replace_measure_contents_03():
    r'''Raise MissingMeasureError when input expression
    contains no measures.
    '''

    note = abjad.Note("c'4")
    notes = [abjad.Note("c'8"), abjad.Note("d'8")]
    note, notes
    statement = 'abjad.mutate(note).replace_measure_contents(notes)'
    assert pytest.raises(abjad.MissingMeasureError, statement)


def test_scoretools_Mutation_replace_measure_contents_04():
    r'''Raise StopIteration when not enough measures.
    '''

    maker = abjad.MeasureMaker()
    measures = maker([(1, 8), (1, 8)])
    staff = abjad.Staff(measures)
    notes = [abjad.Note("c'16"), abjad.Note("d'16"), abjad.Note("e'16"),
        abjad.Note("f'16"), abjad.Note("g'16"), abjad.Note("a'16")]
    notes, staff
    statement = 'abjad.mutate(staff).replace_measure_contents(notes)'
    assert pytest.raises(StopIteration, statement)


def test_scoretools_Mutation_replace_measure_contents_05():
    r'''Populate measures even when not enough total measures.
    '''

    maker = abjad.MeasureMaker()
    measures = maker([(1, 8), (1, 8)])
    staff = abjad.Staff(measures)
    notes = [abjad.Note("c'16"), abjad.Note("d'16"), abjad.Note("e'16"),
        abjad.Note("f'16"), abjad.Note("g'16"), abjad.Note("a'16")]

    try:
        abjad.mutate(staff).replace_measure_contents(notes)
    except StopIteration:
        pass

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 1/8
                c'16
                d'16
            } % measure
            { % measure
                e'16
                f'16
            } % measure
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Mutation_replace_measure_contents_06():
    r'''Preserves ties.
    '''

    maker = abjad.NoteMaker()
    durations = [(5, 16), (3, 16)]
    leaf_lists = maker([0], durations)
    leaves = abjad.sequence(leaf_lists).flatten(depth=-1)

    maker = abjad.MeasureMaker()
    measures = maker(durations)
    staff = abjad.Staff(measures)
    measures = abjad.mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 5/16
                c'4 ~
                c'16
            } % measure
            { % measure
                \time 3/16
                c'8.
            } % measure
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
