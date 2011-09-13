from abjad import *


def test_Measure_special_prolation_01():
    '''Binary measures contribute trivially to contents prolation;
        works on a flat list of notes.'''
    t = Measure((4, 4), Note("c'4") * 4)
    assert t[0].written_duration == Duration(1, 4)
    assert t[0].prolated_duration == Duration(1, 4)


def test_Measure_special_prolation_02():
    '''Binary measures contribute trivially to contents prolation;
        works on notes and tuplets together.'''
    t = Measure((4, 4), [
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
        Note("c'4")])
    assert t.leaves[0].written_duration == Duration(1, 4)
    assert t.leaves[0].prolated_duration == Duration(1, 4)
    assert t.leaves[1].written_duration == Duration(1, 4)
    assert t.leaves[1].prolated_duration == Duration(1, 6)


def test_Measure_special_prolation_03():
    '''Binary measures contribute trivially to contents prolation;
        works on notes and nested tuplets together.'''
    t = Measure((4, 4), [
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(2, 4), [
            tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
            Note("c'4")]),
        Note("c'4")])
    assert t.leaves[0].written_duration == Duration(1, 4)
    assert t.leaves[0].prolated_duration == Duration(1, 4)
    assert t.leaves[1].written_duration == Duration(1, 4)
    assert t.leaves[1].prolated_duration == Duration(1, 9)


def test_Measure_special_prolation_04():
    '''Nonbinary measures contribute nontrivially to contents prolation;
        works on a flat list of notes.'''
    t = Measure((4, 5), Note("c'4") * 4)
    assert t[0].written_duration == Duration(1, 4)
    assert t[0].prolated_duration == Duration(1, 5)


def test_Measure_special_prolation_05():
    '''Nonbinary measures contribute trivially to contents prolation;
        works on notes and tuplets together.'''
    t = Measure((4, 5), [
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
        Note("c'4")])
    assert t.leaves[0].written_duration == Duration(1, 4)
    assert t.leaves[0].prolated_duration == Duration(1, 5)
    assert t.leaves[1].written_duration == Duration(1, 4)
    assert t.leaves[1].prolated_duration == Duration(2, 15)


def test_Measure_special_prolation_06():
    '''Nonbinary measures contribute nontrivially to contents prolation;
        works on notes and nested tuplets together.'''
    t = Measure((4, 5), [
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(2, 4), [
            tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
            Note("c'4")]),
        Note("c'4")])
    assert t.leaves[0].written_duration == Duration(1, 4)
    assert t.leaves[0].prolated_duration == Duration(1, 5)
    assert t.leaves[1].written_duration == Duration(1, 4)
    assert t.leaves[1].prolated_duration == Duration(4, 45)
